import numpy as np
from torch import nn
import torch as th
from google.cloud import storage

import functions_framework

# Custom Model
class NutriNet(nn.Module):
    def __init__(self, input_features, output_features):
        super().__init__()
        self.block1 = nn.Sequential(
            nn.Linear(input_features, 512),
            nn.BatchNorm1d(512),
            nn.ReLU(),
            nn.Linear(512, 512),
            nn.BatchNorm1d(512),
            nn.ReLU(),
            nn.Linear(512, 512),
            nn.Dropout(0.25),
        )
        self.block2 = nn.Sequential(
            nn.Linear(512, 256),
            nn.BatchNorm1d(256),
            nn.ReLU(),
            nn.Linear(256, 256),
            nn.BatchNorm1d(256),
            nn.ReLU(),
            nn.Linear(256, 256),
            nn.Dropout(0.25),
        )
        self.block3 = nn.Sequential(
            nn.Linear(256, 128),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.Dropout(0.25),
        )
        self.block4 = nn.Sequential(
            nn.Linear(128, 64),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.Dropout(0.25),
        )
        self.block5 = nn.Sequential(
            nn.Linear(64, 32),
            nn.BatchNorm1d(32),
            nn.ReLU(),
            nn.Linear(32, 32),
            nn.BatchNorm1d(32),
            nn.ReLU(),
            nn.Linear(32, 6),
        )

    def forward(self, x):
        out = self.block1(x)
        out = self.block2(out)
        out = self.block3(out)
        out = self.block4(out)
        out = self.block5(out)
        return out


# We keep model as global variable so we don't have to reload it in case of warm invocations
model = None

# Function to load model
def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    blob.download_to_filename(destination_file_name)

    print("Blob {} downloaded to {}.".format(source_blob_name, destination_file_name))


# Entry function
@functions_framework.http
def handler(request):
    global model
    # CORS HEADER
    if request.method == "OPTIONS":
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET,POST",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Max-Age": "3600",
        }

        return ("", 204, headers)

    # REAL FUNCTION
    download_blob(
        "thecrapbucket", "torchmodels/nutrinet_trained_1000.pth", "/tmp/nutrinet.pth"
    )
    model = NutriNet(13, 6)
    model.load_state_dict(th.load("/tmp/nutrinet.pth"))

    request_json = request.get_json()
    print(request_json)
    x = []

    # Digit encode gender
    x.append(float(request_json["patient_age"]))
    if request_json["patient_gender"] == "Male":
        x.append(float(1))
    else:
        x.append(float(0))
    # Data prep for single inference
    x.append(float(request_json["height"]))
    x.append(float(request_json["weight"]))
    x.append(float(request_json["hb"]))
    x.append(float(request_json["urea"]))
    x.append(float(request_json["cr"]))
    x.append(float(request_json["na"]))
    x.append(float(request_json["potassium"]))
    x.append(float(request_json["fbs"]))
    x.append(float(request_json["hba1c"]))
    x.append(float(request_json["sgot"]))
    x.append(float(request_json["sgpt"]))
    x = th.Tensor(x)
    # Run single inference on model
    model.eval()
    predictions = model(x.unsqueeze(0))
    predictions = predictions.detach().numpy().squeeze().tolist()

    result = {
        "cal": round(predictions[0], 2),
        "cho": round(predictions[1], 2),
        "fat": round(predictions[2], 2),
        "pro": round(predictions[3], 2),
        "fluids": round(predictions[4], 2),
        "sodium": round(predictions[5], 2),
    }

    # Set CORS headers for the main request
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET,POST",
    }

    return (result, 200, headers)

# imports
import base64 as bs
import speech_recognition as sr
from difflib import SequenceMatcher as sm
import speech_recognition as sr
from difflib import SequenceMatcher as sm
from pydub import AudioSegment
import wave
import contextlib
import functions_framework


@functions_framework.http
def handler(request):  # entry function for cloud function
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

    request_json = request.get_json()
    print(request_json)
#JSON Parsing
    b64str = request_json["basestr"]
    orgstr = request_json["original"]
    reqduration = float(request_json["duration"])

    b64str = b64str[b64str.index(",") + 1 :]
    decode_bytes = bs.b64decode(b64str)

# Export base64 to .ogx
    with open("/tmp/test" + ".ogx", "wb") as wav_file:
        wav_file.write(decode_bytes)

    # Open the ogx file with pydub
    audio = AudioSegment.from_file("/tmp/test.ogx", format="ogg")

    # Export the audio as wav
    audio.export("/tmp/test.wav", format="wav")

    #Calculate the duration of audio
    fname = "/tmp/test.wav"
    with contextlib.closing(wave.open(fname, "r")) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        actual_duration = frames / float(rate)
    
    # Perform text to speech
    r = sr.Recognizer()
    # Reading Audio file as source
    #  listening  the  аudiо  file  аnd  stоre  in  аudiо_text  vаriаble
    with sr.AudioFile("/tmp/test.wav") as source:
        audio_text = r.listen(source)
        # recoginize_() method will throw a request error if the API is unreachable, hence using exception handling
        try:
            # using google speech recognition
            text = r.recognize_google(audio_text)
            print("Converting audio transcripts into text ...")
            print(text)
        except:
            print("Sorry.. run again...")

    # Score calculation with weights
    acc = sm(None, text, orgstr).ratio()
    accw = 0.7
    timew = 0.3
    score = (acc * accw) + ((reqduration / actual_duration) * timew)
    score *= 100
    score = score if score < 100 else 100
    print(score)

    # Return JSON
    result = {"score": score,
              "acc":acc,
              "tm":actual_duration
              }

    # Set CORS headers for the main request
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET,POST",
    }

    return (result, 200, headers)

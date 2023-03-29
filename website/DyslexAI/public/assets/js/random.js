var para=[]
para[0]="The sun was setting over the horizon, casting a warm glow over the landscape. The trees swayed gently in the breeze as a flock of birds flew overhead. A lone figure could be seen walking along the path, their footsteps crunching on the gravel. They stopped to take in the view, breathing in the fresh air and feeling a sense of calm wash over them.";
para[1]="The city streets were bustling with activity, people hurrying to and fro as they went about their daily business. The sound of car horns and chatter filled the air as the sun beat down on the concrete jungle. A street musician sat on the corner, strumming his guitar and singing a soulful tune. Tourists snapped photos of the iconic buildings and landmarks, eager to capture the moment.";
para[2]="The storm raged on outside, lightning illuminating the darkened room as the wind howled through the trees. The family huddled together under blankets, listening to the rain pelt against the roof. Suddenly, the power went out, plunging them into darkness. They lit candles and told stories to pass the time, grateful for each other's company in the midst of the storm.";
para[3]="The beach was a hive of activity, with children building sandcastles and playing in the surf. A group of friends played volleyball, their laughter carrying over the sound of the crashing waves. Couples strolled hand in hand along the shoreline, enjoying the sunshine and salty breeze. A lone fisherman stood at the water's edge, patiently waiting for a bite on his line.";
para[4]="The library was a quiet sanctuary, with rows upon rows of books lining the shelves. The smell of old pages filled the air as patrons flipped through the pages of their favorite novels. A student sat at a table, pouring over textbooks and taking notes. A librarian pushed a cart of returned books, carefully reshelving each one in its proper place.";

var dur=[]
dur[0]="19.00";
dur[1]="21.50";
dur[2]="21.00";
dur[3]="20.50";
dur[4]="21.00";

function parag()
{
    var randompara=Math.floor(Math.random()*(para.length));
    document.getElementById('para').value= para[randompara];
    document.getElementById('dura').value= dur[randompara];
    document.getElementById('prandom').innerHTML= para[randompara];
}
import os
import json
import kveta

DATADIR = "/net/projects/EduPo/data/KCV_komplet/ccv/"

#for fname in sorted(os.listdir(DATADIR)):
for number in range(12508, 20000):
    filename = DATADIR + str(number) + ".json"
    if os.path.isfile(filename) and filename.endswith(".json"):
        f = open(filename)
        data = json.load(f)
        print("Testuji soubor", filename, flush=True)
        text = ""
        for i in range(len(data[0]["body"])):
            for j in range(len(data[0]["body"][i])):
                text += data[0]["body"][i][j]["text"] + "\n"
            text += "\n"
        kveta.okvetuj(text)






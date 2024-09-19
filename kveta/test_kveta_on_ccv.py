import os
import json
import kveta

DATADIR = "/net/projects/EduPo/data/KCV_komplet/ccv/"

for fname in sorted(os.listdir(DATADIR)):
    if os.path.isfile(DATADIR+fname) and fname.endswith(".json"):
        f = open(DATADIR+fname)
        data = json.load(f)
        print("Testuji soubor", fname, flush=True)
        text = ""
        for i in range(len(data[0]["body"])):
            for j in range(len(data[0]["body"][i])):
                text += data[0]["body"][i][j]["text"] + "\n"
            text += "\n"
        kveta.okvetuj(text)






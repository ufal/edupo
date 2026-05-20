import json
import os

for n in range(1,80229):
    filename = "/net/projects/EduPo/data/KCV_analyzed/"+str(n)+".json"
    if not os.path.exists(filename):
        continue
    f = open(filename, "r")
    data = json.load(f)
    count_m = 0
    count_f = 0
    for i in range(len(data[0]["body"][0])):
        if 'narrators_gender' in data[0]["body"][0][i]:
            if data[0]["body"][0][i]['narrators_gender'] == 'M':
                count_m += 1
            elif data[0]["body"][0][i]['narrators_gender'] == 'F':
                count_f += 1

    
    if count_m + count_f  > 0:
        gender = "?"
        if count_m > count_f * 2:
            gender = 'M'
        elif count_f > count_m * 2:
            gender = 'F'
        print(n, count_m, count_f, gender)
    f.close()


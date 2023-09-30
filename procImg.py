import os
import shutil
import math
import pytesseract
from PIL import Image, ImageEnhance

def procImg(path, isEven, filename):
    # ? Cursor
    x = 262
    y = 170
    def_x = 261  # ? The Default cursur start point

    im = Image.open(path)
    enhancer = ImageEnhance.Brightness(im)
    im_output = enhancer.enhance(1.5)
    pix = im_output.load()

    while not pix[x, y] == (0, 0, 0):
        x = x+1
    diffrence = x - def_x - 2

    output = {}

    x = def_x
    y = 308  # 252

    col_i = 1

    def col(col_i, x, y, def_x, output, diffrence):
        print(col_i)
        if (col_i == 6):
            return
        
        x = 261
        def_x = 261
        dat = {}
        formattedDat = {}

        if isEven:
            x = 345
            def_x = 345
        # ? Get {dat}
        #! While cursor on x axis is not at the end:
        # * New sub {i + 1}
        # * Move curor 1 px to left
        # * Set default cursur start point to cur x axis
        #! If i is white:
        # * Move cursor left
        # * Save {dat}
        i = 0
        while not x >= 2303:
            i = i + 1
            x = x + 1
            def_x = x
            while pix[x, y][0] >= 250:
                x = x+1

            x = x+1
            dat[str(i)] = {"x": x, "y": y,
                           "length": math.floor((x-def_x)/diffrence)}
            print(str(i) + " - " +
                  str({"x": x, "y": y, "length": math.floor((x-def_x)/diffrence)}))

        # ? If there is an existing temp folder, remove
        # ? Create new temp dir
        if os.path.exists("./temp"):
            shutil.rmtree("./temp")
        os.mkdir("./temp")

        # ? Crop and save first sub
        t = im.crop((
            261,
            dat["1"]["y"]+100,
            dat["1"]["x"],
            dat["1"]["y"]+152
        ))
        t.save("./temp/1.png")

        # ? Crop and save rest
        for i in dat:
            # ! I know there is a better way of doing this; i lazy
            if (dat.get(str(int(i) + 1))):
                t = im.crop((
                    dat[i]["x"],
                    dat[i]["y"]+100,
                    dat[str(int(i) + 1)]["x"],
                    dat[i]["y"]+152
                ))
                t.save("./temp/"+str(int(i)+1)+'.png')
                print("Cropped and saved ./temp/"+str(int(i)+1)+'.png')

        # ? Get all sub names in each cropped image
        subjs = os.listdir("./temp/")
        for i in subjs:
            name = pytesseract.image_to_string(Image.open("./temp/"+i))
            print("Adding Name: "+name.replace("\n", ""))
            dat[str(i.replace(".png", ""))
                ]["Name"] = name.replace("\n", "")

        # ? -----
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        timeArray = []
        time = [8, 0]
        curp = 0

        total = ""
        for i in time:
            if len(str(i)) == 2:
                total += str(i)
            else:
                total += "0" + str(i)
        timeArray.append(total)
    
        for subi in dat:
            subj = dat[subi]
            for x in range(subj["length"]):
                if not (curp % 2 == 0):
                    time[1] = time[1] + 15
                    if time[1] >= 60:
                        time[0] += 1
                        time[1] -= 60
                else:
                    time[1] += 20
                    if time[1] >= 60:
                        time[0] += 1
                        time[1] -= 60
                curp = + curp + 1

            total = ""
            for i in time:
                if len(str(i)) == 2:
                    total += str(i)
                else:
                    total += "0" + str(i)
            timeArray.append(total)

        formattedDat[timeArray.__getitem__(0)] = dat["1"]["Name"]
        for subi in dat:
            if not (dat.get(str(int(subi) + 1))):
                continue
            subj = dat[str(int(subi) + 1)]
            print(dat)
            if (not subj["Name"] == ""):
                formattedDat[timeArray.__getitem__(int(subi))] = subj["Name"]
                if not (dat.get(str(int(subi) + 2))):
                    continue

                if (dat[str(int(subi) + 2)]["Name"] == ""):
                    formattedDat[timeArray.__getitem__(int(subi) + 1)] = "Null"
                    continue

                if (dat[list(dat)[-1]]["Name"] == dat[str(int(subi) + 2)]["Name"]):
                    formattedDat[timeArray[-1]] = "Null"
                    continue

        print(formattedDat)
        output[days[col_i-1]] = formattedDat

        y = y + 253
        col_i = col_i + 1
        col(col_i, x, y, def_x, output, diffrence)

    col(col_i, x, y, def_x, output, diffrence)

    for day in output:
        if not (day == "Wednesday" or day == "Friday"):
            continue
        d = output[day]
        print(d)
        d.pop("0800")
        output[day] = d
        if os.path.exists("./temp"):
            shutil.rmtree("./temp")

    if not os.path.exists("./output/"):
        os.mkdir("./output/")
    if isEven:
        f = open("./output/"+filename+"_Even.json", "w")
    else:
        f = open("./output/"+filename+"_Odd.json", "w")
    f.write(str(output).replace("\'", "\""))
    f.close()
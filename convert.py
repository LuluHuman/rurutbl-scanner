def convert():
    import os
    import shutil
    import pdf2image

    if os.path.exists("./pages"): shutil.rmtree("./pages")

    os.mkdir("./pages")
    os.mkdir("./pages/odd")
    os.mkdir("./pages/even")

    #Get images
    print("Converting...")
    pdf2image.convert_from_path('file.pdf', fmt="jpeg", output_folder="./pages")
    print("Converted")

    pages = os.listdir("./pages")

    oddtally = 0
    eventally = 0
    for i in pages:
        if (i == "odd" or i == "even"): continue
        n = i.split("-")[5]

        if int(n.replace(".jpg","")) % 2 >= 1:
            oddtally = oddtally + 1
            os.rename("./pages/"+i, "./pages/odd/"+str(oddtally)+".jpg")
        else:
            eventally = eventally + 1
            os.rename("./pages/"+i, "./pages/even/"+str(eventally)+".jpg")
        print("Sorted ./pages/"+i)
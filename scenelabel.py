from deepdanbooru_onnx import DeepDanbooru
import os
import sys
import argparse
import shutil
import subprocess
import pandas as pd

danbooru = DeepDanbooru(pin_memory=True)

def main(opt):
    if os.path.isdir(opt.input): #process a directory
        for filename in os.listdir(opt.input):
            if filename.endswith((".mp4",".mkv",".avi",".mpg",".mov",".mpeg",".wmv",".ogm",".m2ts",".vob",".avs")):
                ClearTemp()
                fullpath = os.path.join(opt.input,filename)
                print("Processing " + fullpath + "...")
                subprocess.run(["scenedetect", "-i", fullpath, "detect-adaptive", "list-scenes", "-f", filename, "save-images", "-o", "temp", "-n", "1", "-h", "512"])
                csv = pd.read_csv(filename + ".csv", header=1, usecols=["Scene Number", "Start Frame", "Start Timecode"]) #read csv file
                csv["Booru Tags"] = "" #add extra column for tags
                GetBooruTags(csv).to_csv(filename + ".csv", index=False)
                if opt.keep_thumbs:
                    if os.path.exists(filename + "-thumbs"):
                        shutil.rmtree(filename + "-thumbs")
                    shutil.copytree("temp",filename + "-thumbs")

    else: #process a single file
        ClearTemp()
        filename = os.path.basename(opt.input)
        print("Processing " + filename + "...")
        subprocess.run(["scenedetect", "-i", opt.input, "detect-adaptive", "list-scenes", "-f", filename, "save-images", "-o", "temp", "-n", "1", "-h", "512"])
        csv = pd.read_csv(filename + ".csv", header=1, usecols=["Scene Number", "Start Frame", "Start Timecode"]) #read csv file
        csv["Booru Tags"] = "" #add extra column for tags
        GetBooruTags(csv).to_csv(filename + ".csv", index=False)
        if opt.keep_thumbs:
            if os.path.exists(filename + "-thumbs"):
                shutil.rmtree(filename + "-thumbs")
            shutil.copytree("temp", filename + "-thumbs")

def ClearTemp():
    if not os.path.exists("temp"):
        os.mkdir("temp")
    for filename in os.scandir("temp"): 
        os.remove(filename.path) #empty the temp directory

def GetBooruTags(csv):
    count = -1
    for filename in os.listdir("temp"):
        if filename.endswith(".jpg"):
            count+=1
            image = os.path.join("temp", filename)
            print("getting booru tags for scene " + str(count+1))
            tag_dict = danbooru(image)
            keysList = list(tag_dict.keys())
            csv.at[count,'Booru Tags']=keysList
    return csv

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help="a video file or a folder containing video files")
    parser.add_argument('-k', '--keep-thumbs', action='store_true', default=False, help="keep generated thumbnails in a folder named after each video file")
    opt = parser.parse_args()
    main(opt)
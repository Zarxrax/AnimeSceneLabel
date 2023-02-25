from deepdanbooru_onnx import DeepDanbooru
import os
import argparse
import shutil
import subprocess
import pandas as pd
import tempfile

danbooru = DeepDanbooru()

def main(opt):
    with tempfile.TemporaryDirectory() as tmpdirname:
        filelist=[]
        if os.path.isdir(opt.input): #process a directory
            for filename in os.listdir(opt.input):
                if filename.endswith((".mp4",".mkv",".avi",".mpg",".mov",".mpeg",".wmv",".ogm",".m2ts",".vob",".avs")):
                    filelist.append(os.path.join(opt.input,filename))
        else: #process a single file
            filelist.append(opt.input)
        for filename in filelist:
            ProcessVideo(filename, tmpdirname)
            for filename in os.scandir(tmpdirname): 
                os.remove(filename.path) #empty the temp directory

def ProcessVideo(filename, tmpdirname):
    print("Processing " + filename + "...")
    out_filename = filename
    if opt.output:
        if not os.path.exists(opt.output):
            os.mkdir(opt.output)
        out_filename = os.path.join(opt.output, os.path.basename(filename))
    subprocess.run(["scenedetect", "-i", filename, "detect-adaptive", "list-scenes", "-f", out_filename, "save-images", "-o", tmpdirname, "-n", "1", "-w", "512", "-h", "512"])
    csv = pd.read_csv(out_filename + ".csv", header=1, usecols=["Scene Number", "Start Frame", "Start Timecode"]) #read csv file
    csv["Booru Tags"] = "" #add extra column for tags
    csv = GetBooruTags(csv, tmpdirname)
    csv.to_csv(out_filename + ".csv", index=False)
    print("Saved tags to " + out_filename + ".csv")
    if opt.keep_thumbs:
        if os.path.exists(out_filename + "-thumbs"):
            shutil.rmtree(out_filename + "-thumbs")
        shutil.copytree(tmpdirname,out_filename + "-thumbs")
        print("Copied thumbnails to " + out_filename + "-thumbs")

def GetBooruTags(csv, tmpdirname):
    count = -1
    for filename in os.listdir(tmpdirname):
        if filename.endswith(".jpg"):
            count+=1
            image = os.path.join(tmpdirname, filename)
            print("Getting booru tags for scene " + str(count+1) + "     ", end='\r')
            tag_dict = danbooru(image)
            keysList = list(tag_dict.keys())
            csv.at[count,'Booru Tags']=keysList
    print("")
    return csv

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help="a video file or a folder containing video files")
    parser.add_argument('-o', '--output', help="a directory to store cvs files and thumbnails")
    parser.add_argument('-k', '--keep-thumbs', action='store_true', default=False, help="keep generated thumbnails in a folder named after each video file")
    opt = parser.parse_args()
    main(opt)
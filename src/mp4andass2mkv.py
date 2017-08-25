#!/usr/bin/env python3
#ffmpeg -i $SHOWFILENAME.mp4 -i $SHOWFILENAME.enUS.ass -map 0 -map 1 -c copy -metadata:s:s:0 language=eng -disposition:s:0 default $SHOWFILENAME.mkv
#ffmpeg -i $SHOWFILENAME.mp4 -map 0 -vcodec libx264 -vf "ass=$SHOWFILENAME.enUS.ass" $SHOWFILENAME.mkv
import platform
import subprocess
import sys

outputMKVFile = "Output.mkv"
hardEncodeSubtitles = False

#Assign appropriate ffmpeg executable name for user's operating system
userOperatingSystem = platform.system()
if userOperatingSystem == "Linux":
    ffmpegBinary = "ffmpeg"
elif userOperatingSystem == "Windows":
    ffmpegBinary = "ffmpeg.exe"
else:
    print("Unsupported Operating System")
    quit(1)

print("\"" + sys.argv[1] + "\" is the selected file\n")

for argumentItem in sys.argv[1:]:
    if argumentItem == "--hardsub":
        hardEncodeSubtitles = True
        print("Hardsubbing Mode Enabled\n")

try:
    inputVideoFile = sys.argv[1]
except:
    print("Argument Error")
    quit(1)
else:
    if inputVideoFile.endswith(".mp4"):
        inputSubtitleFile = inputVideoFile[:-4] + ".enUS.ass"
    else:
        print("File Extension Error")
        quit(1)
    outputMKVFile = inputVideoFile[:-4] + ".mkv"

print("\n")
if hardEncodeSubtitles == False:
    subprocess.run([ffmpegBinary, "-i", inputVideoFile, "-i", inputSubtitleFile, "-map", "0", "-map", "1", "-c", "copy", "-disposition:s:0", "default", outputMKVFile])
else:
    #ffmpeg -i $SHOWFILENAME.mp4 -map 0 -vcodec libx264 -vf "ass=$SHOWFILENAME.enUS.ass" $SHOWFILENAME.mkv
    hardsubOption = "subtitles=" + inputSubtitleFile + ":force_style='FontName=Ubuntu'"
    print(hardsubOption)
    ffmpegOptions = [ffmpegBinary, "-i", inputVideoFile, "-map", "0", "-vcodec", "libx264", "-vf", hardsubOption, "-acodec", "copy", outputMKVFile]
    print(ffmpegOptions)
    subprocess.run(ffmpegOptions)


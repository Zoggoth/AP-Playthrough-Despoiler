import glob
import re
import os
import fnmatch
import yaml
from urllib.request import urlopen
from html import unescape
import random

print("Program for fixing Archipelago runs where everyone thinks they're BK.")
print("Compares the spoiler log's playthrough to the AP Sphere Tracker & prints the missing checks.")
print("Can reveal 1 check at a time, 1 sphere at a time, or all at once (see settings.yaml).")
print("Sphere tracker link & spoiler file should also be listed in settings.yaml.")
print("Events that appear in the spoiler log but not in the sphere tracker cannot be automatically detected.")
print("To remove them, they must be listed in events.txt.")
print()
file = open("settings.yaml")
settings = yaml.safe_load(file)
tracker = settings["Sphere Tracker Link"]
if tracker == "":
    print("No sphere tracker link in settings.yaml.")
    print("The sphere tracker is available from the room info page.")
    input()
    quit()
printWholeSphere = settings["Whole Sphere"]
filename = settings["Spoiler File Name"]
displayItemNames = settings["Display Item Names"]
file.close()
file = open("events.txt")
eventList = set(file.read().splitlines())
file.close()
if filename == "":
    # first search for filenames using the standard format (folder recursive)
    result = []
    for root, dirs, files in os.walk(os.getcwd()):
        for name in files:
            if fnmatch.fnmatch(name, '*Spoiler.txt'):
                result.append(os.path.join(root, name))
    if len(result) == 0:
        # if none are found, search all text files. (not recursive, to avoid random files)
        result = glob.glob('*.txt')
        result.remove('events.txt')
        if len(result) == 0:
            print("No spoiler file found. Spoiler files are on the Seed Info page if generated online, or in the .zip output files if generated locally. Please move it into {}".format(os.getcwd()))
            input()
            quit()
    if len(result) >= 2:
        print(result)
        print("Multiple spoiler files found. Please delete old spoiler files, or specify which file should be used in settings.yaml")
        input()
        quit()
    filename = result[0]
page = urlopen(tracker)
html_bytes = page.read()
html = unescape(html_bytes.decode("utf-8"))
checkedMatches = re.findall("<tr>\\n *<td>\d+<\/td>\\n *<td>(.*?)<\/td>\\n *<td>.*?<\/td>\\n *<td>.*?<\/td>\\n *<td>(.*?)<\/td>",html)
checkedSet = set()
for x in checkedMatches:
    checkedSet.add("{} ({})".format(x[1],x[0]))
file = open(filename)
text = file.read()
playthroughText = re.search("Playthrough:\n\n(\d+: {(.*\n)*?}\n)*",text)[0]
sphereMatches = re.findall("\d+: {\n((?:.*\n)*?)}",playthroughText)
spheres = []
currentSphere = 0
match printWholeSphere:
    case 0: print("Playthrough (Single Check Mode. Press Enter to Continue)")
    case 1: print("Playthrough (Sphere Mode. Press Enter to Continue)")
    case _: print("Playthrough (Complete Mode)")
print()
for x in sphereMatches:
    checkMatches = re.findall("  ((.*? \(.*?\)): (.*?) \(.*?\))\n",x)
    toPrint = []
    for y in checkMatches:
        checkName = re.search("^(.*) \([^()]*(?:\(.*\))*\)$", y[1])
        if y[2] == "Victory":  # Some victory events (e.g Yacht Dice) have to be identified by item instead of location
            continue
        if checkName[1] in eventList:
            continue
        if checkName[0] in checkedSet:
            continue
        if displayItemNames:
            toPrint.append(y[0])
        else:
            toPrint.append(y[1])
    if len(toPrint) > 0:
        if printWholeSphere == 0:
            random.shuffle(toPrint)
        if printWholeSphere <= 1:
            input("Sphere {}:".format(currentSphere))
        else:
            print("Sphere {}:".format(currentSphere))
        for y in toPrint:
            if printWholeSphere == 0:
                input(y)
            else:
                print(y)
        print()
    currentSphere += 1
input("Done!")
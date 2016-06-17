#!/usr/bin/env python3

import os
import time
import shutil, errno

# start setup part
templateStart = "% start"
templateStop = "% stop"
partsDir = "./parts"
outputDir = "./out"
outputFile = "Mathe2_SoSe16.tex"
templateDir = "./"
templateFile = "template.tex"
# stop setup part

class Part:
    def __init__(self, name, creation):
        self.name = name
        self.creation = creation
        self.lines = []

parts = []
directories = []
for filename in sorted(os.listdir(partsDir)):
    filePath = os.path.join(partsDir, filename)
    if os.path.isfile(filePath) and filename.endswith(".tex"):
        file = open(filePath, "r")
        startFound = False
        for line in file:
            if line.strip() == templateStart:
                part = Part(filename, time.ctime(os.path.getctime(filePath)))
                startFound = True
            elif startFound and line.strip() == templateStop:
                parts.append(part)
                break
            elif startFound:
                part.lines.append(line)
        file.close()
    if os.path.isdir(filePath):
        directories.append(filename)

template = open(os.path.join(templateDir, templateFile), "r")
if os.path.exists(outputDir):
    shutil.rmtree(outputDir)
os.makedirs(outputDir)
output = open(os.path.join(outputDir, outputFile), "w")
startReached = False
for line in template:
    if line.strip() != templateStart and line.strip() != templateStop:
        output.write(line)
    elif line.strip() == templateStart:
        for part in parts:
            output.write(templateStart + " " + part.name + " " + part.creation + os.linesep)
            for line in part.lines:
                output.write(line)
            output.write(templateStop + " " + part.name + " " + part.creation + os.linesep)
output.close()

for directory in directories:
    shutil.copytree(os.path.join(partsDir, directory), os.path.join(outputDir, directory))

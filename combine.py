#!/usr/bin/env python3

import os
import time

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
for dirpath, dirnames, filenames in os.walk(partsDir):
    for filename in filenames:
        filePath = os.path.join(dirpath, filename)
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

template = open(os.path.join(templateDir, templateFile), "r")
if not os.path.exists(outputDir):
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
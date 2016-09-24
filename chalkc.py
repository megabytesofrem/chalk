import re
import sys

class Internals:
    localVars = {}
    def __init__(self):
        pass

class Parser:
    internals = Internals()

    run = True
    mem = []

    def __init__(self):
        pass

    def chomp(self, line):
        return line.replace("\t", "").lstrip()

    def checkVar(self, var):
        if var[0] == "@":
            return self.internals.localVars[var[1:]]

    def parse(self, ln):
        ln = self.chomp(ln)
        line = ln.split(" ")

        if self.run:
            if line[0] == "if":
                self.mem.append("if")
                for i in range(1, 4, 2):
                    checkedVar = self.checkVar(line[i])
                    if checkedVar:
                        line[i] = checkedVar

                if line[2] == "==":
                    #print line[1]
                    #print line[3]
                    if line[1] != line[3]:
                        self.run = False
                elif line[2] == "!=":
                    if line[1] == line[3]:
                        self.run = False
            elif line[0] == "end":
                if line[1] == "if":
                    if self.mem[-1] == "if":
                        del self.mem[-1]
            elif line[0] == "write":
                print " ".join(line[1:])
            elif len(line) == 3:
                self.internals.localVars[line[0]] = line[2]

p = Parser()
for arg in range(0, len(sys.argv)):
    if arg != 0:
        argFile = open(sys.argv[arg], "r")
        argFile = argFile.read().split("\n")
        for line in argFile:
            if line:
                p.parse(line)

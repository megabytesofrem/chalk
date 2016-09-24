import re
import sys

class Internals:
    localVars = {}
    def __init__(self):
        pass

class Parser:
    internals = Internals()

    run = True
    insideLoop = False
    insideSubs = False
    loops = []

    loopStart = 0
    loopEnd = 0
    loopOp = ""
    subs = ""
    mem = []

    def __init__(self):
        pass

    def chomp(self, line):
        return line.replace("\t", "").lstrip()

    def checkVar(self, var):
        if var[0] == "@":
            return self.internals.localVars[var[1:]]

    def error(self, fatal, msg):
        if fatal:
            print "[FATAL] " + msg
            sys.exit()
        else:
            print "[ERROR] " + msg

    def parse(self, ln):
        ln = self.chomp(ln)
        line = ln.split(" ")

        if self.run:
            if line[0] == "if":
                if not self.insideLoop:
                    self.mem.append("if")
                    for i in range(1, 4, 2):
                        checkedVar = self.checkVar(line[i])
                        if checkedVar:
                            line[i] = checkedVar

                    if line[2] == "==":
                        if line[1] != line[3]:
                            self.run = False
                    elif line[2] == "!=":
                        if line[1] == line[3]:
                            self.run = False
                    elif line[2] == ">":
                        if int(line[1]) < int(line[3]):
                            self.run = False
                    elif line[2] == "<":
                        if int(line[1]) > int(line[3]):
                            self.run = False
                    elif line[2] == ">=":
                        if int(line[1]) <= int(line[3]):
                            self.run = False
                    elif line[2] == "<=":
                        if int(line[1]) >= int(line[3]):
                            self.run = False
                    else:
                        self.error(True, "Expected either ==, !=, <, >, <=, >= but got " + line[2])
                else:
                    self.loops.append("if " + line[1] + " " + line[2] + " " + line[3] + " then")

            # for i in 0 .. 10 do
            elif line[0] == "for":
                if line[6] == "do":
                    self.mem.append("for")
                    self.loopStart = int(line[3])
                    self.loopEnd = int(line[5])
                    self.insideLoop = True
                else:
                    self.error(True, "Expected do but got " + line[6])

            # while @a != @b do
            elif line[0] == "while":
                self.mem.append("while")
                if line[1] == "true":
                    self.loopStart = "true"
                elif line[1] == "false":
                    self.loopStart = "false"
                elif line[1][0] == "@":
                    self.loopStart = self.internals.localVars[line[1][1:]]
                else:
                    self.error(True, "Expected either true, false or @name but got " + line[1])

                if line[2] == "!=":
                    self.loopOp = "!="
                elif line[2] == "==":
                    self.loopOp = "=="
                else:
                    self.error(True, "Expected either == or != but got " + line[2])

                if line[3] == "true":
                    self.loopEnd = "true"
                elif line[3] == "false":
                    self.loopEnd = "false"
                elif line[3][0] == "@":
                    self.loopEnd = self.internals.localVars[line[3][1:]]
                else:
                    self.loopEnd = line[3]

                self.insideLoop = True


            elif line[0] == "end":
                if line[1] == "if":
                    if not self.insideLoop:
                        if self.mem[-1] == "if":
                            del self.mem[-1]
                    else:
                        self.loops.append("end if")

                elif line[1] == "for":
                    if self.mem[-1] == "for":
                        del self.mem[-1]
                        self.insideLoop = False

                        for i in range(self.loopStart, self.loopEnd):
                            for loop in self.loops:
                                self.parse(loop)
                        self.loops = []

                elif line[1] == "while":
                    if self.mem[-1] == "while":
                        del self.mem[-1]
                        self.insideLoop = False

                        if self.loopOp == "==":
                            while self.loopStart == self.loopEnd:
                                for loop in self.loops:
                                    self.parse(loop)
                            self.loops = []
                        elif self.loopOp == "!=":
                            while self.loopStart != self.loopEnd:
                                for loop in self.loops:
                                    self.parse(loop)
                            self.loops = []
                        else:
                            self.error(True, "Expected either == or != but got " + self.loopOp)

            elif line[0] == "write":
                if not self.insideLoop:
                    msg = " ".join(line[1:])

                    if msg[0] == "@":
                        print str(self.internals.localVars[msg[1:]].replace('"', "")),
                    else:
                        print str(msg)
                else:
                    self.loops.append("write " + " ".join(line[1:]))

            elif line[0] == "read":
                if not self.insideLoop:
                    pieces = line[1]

                    self.internals.localVars[line[1]] = raw_input("")
                else:
                    self.loops.append("read " + pieces[0] + " " + pieces[1])

            elif len(line) >= 3:
                if line[1] == "=":
                    if line[2][0] == '"' and line[2][len(line) - 1] == '"':
                        self.internals.localVars[line[0]] = line[2].strip('"')
                    elif line[2] == "true" or line[2] == "false":
                        self.internals.localVars[line[0]] = line[2]
                    else:
                        self.internals.localVars[line[0]] = line[2]
                elif line[1] == "+=":
                    if line[2][0] == '"' and line[2][len(line) - 1] == '"':
                        self.internals.localVars[line[0]] += line[2].strip('"')
                    elif line[2] == "true" or line[2] == "false":
                        self.internals.localVars[line[0]] += line[2]
                    else:
                        self.internals.localVars[line[0]] += line[2]
                if line[0][0:1] == "--":
                    pass

                print line
            else:
                self.error(True, "Expected a valid statement but got " + line[0])

p = Parser()
for arg in range(0, len(sys.argv)):
    if arg != 0:
        argFile = open(sys.argv[arg], "r")
        argFile = argFile.read().split("\n")
        for line in argFile:
            if line:
                p.parse(line)

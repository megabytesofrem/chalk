import re
import sys

class Internals:
    localVars = {}
    localFuncs = {}
    def __init__(self):
        pass

class Parser:
    internals = Internals()

    run = True
    insideLoop = False
    insideFunc = False
    loops = []
    blocks = []

    loopStart = 0
    loopEnd = 0
    loopOp = ""
    funcName = ""
    funcParams = []
    mem = []

    def __init__(self):
        pass

    def chomp(self, line):
        return line.replace("\t", "").lstrip()

    def checkVar(self, var):
        if var[0] == "@":
            try:
                return self.internals.localVars[var[1:]]
            except:
                return var
        else:
            return var

    def createFunc(self, name, blocks):
        try:
            return self.internals.localFuncs[name]
        except:
            self.internals.localFuncs[name] = blocks

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
                    if self.insideFunc:
                        self.blocks.append("if " + line[1] + " " + line[2] + " " + line[3] + " then")
                    elif self.insideLoop:
                        self.loops.append("if " + line[1] + " " + line[2] + " " + line[3] + " then")

            # for i in 0 .. 10 do
            elif line[0] == "for":
                if line[6] == "{":
                    self.mem.append("for")
                    self.loopStart = int(line[3])
                    self.loopEnd = int(line[5])
                    self.insideLoop = True
                else:
                    self.error(True, "Expected do but got " + line[6])

            # func x param1,param2 { .. }
            elif line[0] == "func":
                if line[3] == "{":
                    self.mem.append("function")
                    self.funcName = line[1]
                    if line[2] != "none":
                        for i in range(-1, 1):
                            line[2] = list(line[2])
                            line[2][i] = ''
                            line[2] = "".join(line[2])
                        self.funcParams = line[2].split(",")
                    else:
                        self.funcParams = []
                    self.insideFunc = True
                else:
                    self.error(True, "Expected { but got " + line[3])


            # while @a != @b do
            elif line[0] == "while":
                self.mem.append("while")
                if not self.insideFunc:
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
                else:
                    self.blocks.append("while " + line[1] + " " + line[2] + " " + line[3] + "{")


            elif line[0] == "}":
                if not self.insideLoop and len(self.mem) > 0:
                    if self.mem[-1] == "if":
                        del self.mem[-1]
                    elif self.mem[-1] == "for":
                        del self.mem[-1]
                        self.insideLoop = False

                        for i in range(self.loopStart, self.loopEnd):
                            for loop in self.loops:
                                self.parse(loop)
                        self.loops = []
                    elif self.mem[-1] == "while":
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
                    elif self.mem[-1] == "function":
                            del self.mem[-1]
                            self.insideFunc = False
                            self.internals.localFuncs[self.funcName] = [self.funcParams, self.blocks]
            elif line[0] == "write":
                if not self.insideLoop and not self.insideFunc:
                    chopped = line[1:]
                    for word in range(0, len(chopped)):
                        chopped[word] = self.checkVar(chopped[word])

                    print " ".join(chopped)

                if self.insideLoop:
                    self.loops.append("write " + " ".join(line[1:]))

                if self.insideFunc:
                    self.blocks.append("write " + " ".join(line[1:]))

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
                elif line[1] == "-=":
                    if line[2][0] == '"' and line[2][len(line) - 1] == '"':
                        self.internals.localVars[line[0]] -= line[2].strip('"')
                    elif line[2] == "true" or line[2] == "false":
                        self.internals.localVars[line[0]] -= line[2]
                    else:
                        self.internals.localVars[line[0]] -= line[2]
                if line[0][0:1] == "--":
                    pass
            elif line[0] in self.internals.localFuncs:
                if line[1] != "none":
                    for i in range(-1, 1):
                        line[1] = list(line[1])
                        line[1][i] = ''
                        line[1] = "".join(line[1])
                    params = line[1].split(",")
                else:
                    params = []
                for block in self.internals.localFuncs[line[0]][1]:
                    split = block.split(" ")
                    for word in range(0, len(split)):
                        if split[word][0] == "@":
                            try:
                                split[word] = params[self.internals.localFuncs[line[0]][0].index(split[word][1:])]
                            except:
                                print 'Local variable nope basically'
                                pass
                    self.parse(" ".join(split))
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

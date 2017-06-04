import re
import sys

class Internals:
    globalVars = {}
    globalFuncs = {}
    def __init__(self):
        pass

class Parser:
    internals = Internals()
    run = True
    mem = []

    def __init__(self):
        pass

    def chomp(self, line):
        if line[0] == "(" and line[-1] == ")":
            lineSplit = list(line)
            for i in range(-1, 1):
                del lineSplit[i]
            return "".join(lineSplit)
        else:
            return line.replace("\t", "").lstrip()

    def error(self, fatal, msg):
        if fatal:
            print("[FATAL] " + msg)
            sys.exit()
        else:
            print("[ERROR] " + msg)

    def saveGlobalVar(self, name, content):
        self.internals.globalVars[name] = content

    def renderGlobalVar(self, var):
        try:
            return self.internals.globalVars[var]
        except:
            self.error(True, "Undefined variable " + var)

    def renderString(self, line):
        if (line[0] == "\"" and line[-1] == "\""):
            line = line.replace("\"", "")
            lineSplit = line.split(" ")
            for word in range(0, len(lineSplit)):
                if lineSplit[word][0] == "@":
                    lineSplit[word] = str(self.renderGlobalVar(lineSplit[word][1:]))
            return " ".join(lineSplit)
        else:
            print(line)
            self.error(True, "Does not follow string formatting")

    def compare(self, strings, operator):
        run = True
        for i in range(0, 2):
            strings[i] = self.renderString(strings[i])

        if operator == "==":
            if strings[0] != strings[1]:
                run = False
        elif operator == "!=":
            if strings[0] == strings[1]:
                run = False
        elif operator == ">":
            if int(strings[0]) < int(strings[1]):
                run = False
        elif operator == "<":
            if int(strings[0]) > int(strings[1]):
                run = False
        elif operator == ">=":
            if int(strings[0]) <= int(strings[1]):
                run = False
        elif operator == "<=":
            if int(strings[0]) >= int(strings[1]):
                run = False
        else:
            self.error(True, "Expected either ==, !=, <, >, <=, >= but got " + line[2])
            run = None

        if run != None:
            return run

    def parse(self, ln):
        ln = self.chomp(ln)
        line = ln.split(" ")

        if line[0] == "}":
            if len(self.mem) > 0:
                self.run = True
                if self.mem[-1][0] == "function":
                    # globalFunc[function] = [[blocks], [params]]
                    # Function memory entry
                    # mem = ["function", [blocks], [name, [params]]
                    self.internals.globalFuncs[self.mem[-1][2][0]] = [self.mem[-1][1], self.mem[-1][2][1]]
                elif self.mem[-1][0] == "while":
                    # While memory entry
                    # mem = ["while", [blocks], ["true", "==", "true"]]
                    while self.compare([self.mem[-1][2][0], self.mem[-1][2][2]], self.mem[-1][2][1]):
                        for block in self.mem[-1][1]:
                            self.parse(block)

            else:
                self.error(True, "Unexpected end of block")

        elif self.run == False:
            self.mem[-1][1].append(ln)

        # if param = param { .. }
        elif line[0] == "if":
            if line[4] == "{":
                self.mem.append(["if", []])
                self.run = self.compare([line[1], line[3]], line[2])
            else:
                self.error(True, "Expected { but got " + line[4])

        # while param = param { .. }
        elif line[0] == "while":
            if line[4] == "{":
                self.run = False
                self.mem.append(["while", [], [line[1], line[2], line[3]]])
            else:
                self.error(True, "Expected { but got " + line[4])

        # func x (param1,param2) { .. }
        elif line[0] == "func":
            if line[3] == "{":
                params = []
                paramSplit = self.chomp(line[2]).split(",")
                for param in range(0, len(paramSplit)):
                    params.append(paramSplit[param])
                self.run = False
                self.mem.append(["function", [], [line[1], params]])
            else:
                self.error(True, "Expected { but got " + line[3])

        elif line[0] == "write":
            print((self.renderString(" ".join(line[1:]))))

        # read @var
        elif line[0] == "read":
            if line[1][0] == "@":
                read = input()
                self.internals.globalVars[line[1][1:]] = read;

        # Declares a variable
        elif len(line) >= 3:
            if line[1] == "=":
                self.saveGlobalVar(line[0], self.renderString(line[2]))
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

        # Checks for a function
        elif line[0] in self.internals.globalFuncs:
            paramSplit = self.chomp(line[1]).split(",")
            for param in range(0, len(paramSplit)):
                self.saveGlobalVar(self.internals.globalFuncs[line[0]][1][param], self.renderString(paramSplit[param]))
            for block in self.internals.globalFuncs[line[0]][0]:
                self.parse(block)

        # No statment found
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

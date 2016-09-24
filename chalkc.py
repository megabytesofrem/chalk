import re

class Internals:
    def __init__(self):
        pass

    localVars = {}
    localFuncs = {}
    conditionals = {}

class Parser:
    internals = Internals()
    inIfBlock = False
    currentIfCond = ""

    def __init__(self):
        pass

    def chomp(self, line):
        return line.replace("\t", "").lstrip()

    # Lookup a function definition
    # If it exists, call it with the params
    def lookupFunction(name, params):
        pass

    # Parse an if statement
    # If the two values are the same as each other
    # execute all the code between the if and end if
    def parseIf(self, cond, blocks):
        pieces = cond.split(" ")
        a = ""
        b = ""

        op = pieces[1]
        if pieces[0][0] == "@":
            a = self.internals.localVars[pieces[0][1:]]
            if pieces[2][0] == "@":
                b = self.internals.localVars[pieces[2][1:]]
            else:
                b = pieces[2]
        else:
            a = pieces[0]

        if op == "==":
            if a == b:
                for line in blocks:
                    self.parse(line)
            else:
                print "False"

        if op == "!=":
            if a != b:
                for line in blocks:
                    self.parse(line)
            else:
                print "False"

    def parse(self, ln):
        conditionalsStack = []
        counter = 0

        line = self.chomp(ln)
        assign = re.match(r"([a-z]+)\s=+\s(.+)", line)
        write = re.match(r"write\s(.+)", line)

        funcCall = re.match(r"([a-z]+)+\((.*)\)", line)
        ifBegin = re.match(r"if\s(.+)\s(==|!=)\s(.+)\sthen", line)
        ifEnd = re.match(r"end\sif", line)

        # variable assignent
        if assign:
            variable = assign.groups()[0] + " = " + assign.groups()[1]
            if self.inIfBlock:
                items = self.internals.conditionals[self.currentIfCond]
                self.internals.conditionals[self.currentIfCond].append(variable)
            else:
                print "assigned %s to %s" % (assign.groups()[0], assign.groups()[1])
                self.internals.localVars[assign.groups()[0]] = assign.groups()[1]

        # write statement
        if write:
            string = write.groups()[0]
            call = "write " + string
            if self.inIfBlock:
                items = self.internals.conditionals[self.currentIfCond]
                self.internals.conditionals[self.currentIfCond].append(call)
            else:
                print string

        # function call
        if funcCall:
            call = funcCall.groups()[0] + "(" + funcCall.groups()[1] + ")"
            if self.inIfBlock:
                items = self.iternals.conditionals[self.currentIfCond]
                self.internals.conditionals[self.currentIfCond].append(call)
            else:
                print call
            #print funcCall.groups()

        # if statement
        if ifBegin:
            conditionalsStack.append(ifBegin.groups()[0] + " " + ifBegin.groups()[1] + " " + ifBegin.groups()[2])

            print conditionalsStack
            self.inIfBlock = True
            self.currentIfCond = conditionalsStack[counter]
            self.internals.conditionals[ifBegin.groups()[0] + " " + ifBegin.groups()[1] + " " + ifBegin.groups()[2]] = []

            #print self.internals.conditionals[ifBegin.groups()[0] + " " + ifBegin.groups()[1] + " " + ifBegin.groups()[2]]
            print ifBegin.groups()

        if ifEnd:
            self.inIfBlock = False
            self.parseIf(self.currentIfCond, self.internals.conditionals[self.currentIfCond])

            #print self.internals.conditionals[self.currentIfCond]
            counter += 1
            print "end if"

p = Parser()
p.parse("print()")
p.parse("a = 10")
p.parse("b = 10")
p.parse("if @a == @b then")
p.parse("write Hello!")
p.parse("   if @b != 11 then")
p.parse("       write true")
p.parse("   end if")
p.parse("end if")

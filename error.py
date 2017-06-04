import sys

fatalExceptions = ["UndefinedVariable", "UndefinedStatement", "SyntaxError", "ParserError"]

def throwFatal(exception, msg):
    if exception in fatalExceptions:
        print("[" + exception + "] " + msg)
    else:
        print("[ParserError] Invalid exception thrown")
    sys.exit()

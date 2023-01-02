#!/usr/bin/python3
"""
    Write a script markdown2html.py that takes an argument 2 strings:
    First argument is the name of the Markdown file
    Second argument is the output file name
"""
if __name__ == "__main__":
    import sys
    from os import path
    import re
    import hashlib

    md = {"#": "h1", "##": "h2", "###": "h3", "####": "h4", "#####": "h5",
          "######": "h6", "-": "ul", "*": "ol"}

    if len(sys.argv) < 3:
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        exit(1)

    if not path.exists(sys.argv[1]) or not str(sys.argv[1]).endswith(".md"):
        sys.stderr.write("Missing " + sys.argv[1] + '\n')
        exit(1)

    def headings(pattern):
        x = md[lineSplit[0]]
        Write = line.replace("{} ".format(lineSplit[0]), "<{}>".format(x))
        Write = Write[:-1] + ("</{}>\n".format(x))
        fw.write(Write)

    def inlineMarkdown(line, pattern):
        y = 0
        while pattern in line:
            if not y:
                if pattern == "**":
                    line = line.replace(pattern, "<b>", 1)
                    y = 1
                else:
                    line = line.replace(pattern, "<em>", 1)
                    y = 1
            else:
                if pattern == "**":
                    line = line.replace(pattern, "</b>", 1)
                    y = 0
                else:
                    line = line.replace(pattern, "</em>", 1)
                    y = 0
        return line

    def md5Markdown(line):
        rep = []
        while "[[" in line and "]]" in line:
            rep = []
            for j in range(len(line)):
                if not j == len(line) - 1 and line[j] == '[' and\
                        line[j + 1] == '[':
                    rep.append(j)
                elif not j == len(line) - 1 and line[j] == "]" and \
                        line[j + 1] == ']':
                    rep.append(j)
            if rep:
                sliceObj = slice(rep[0], rep[1] + 2)

            toRep = line[sliceObj]
            toHash = toRep[2:-2]
            md = hashlib.md5(toHash.encode()).hexdigest()
            line = line.replace(toRep, md)
        return line

    def caseMarkdown(line):
        rep = []
        s = ''
        while '((' in line:
            rep = []
            for j in range(len(line)):
                if not j == len(line) - 1 and line[j] == '(' and\
                        line[j + 1] == '(':
                    rep.append(j)
                elif not j == len(line) - 1 and line[j] == ")" and\
                        line[j + 1] == ')':
                    rep.append(j)
            if rep:
                sliceObj = slice(rep[0], rep[1] + 2)
            toRep = line[sliceObj]
            s = toRep
            for char in toRep:
                if char == 'c':
                    toRep = toRep.replace('c', '')
                elif char == 'C':
                    toRep = toRep.replace('C', '')
            line = line.replace(s, toRep[2:-2])
        return line

    with open(sys.argv[1], mode='r') as fr, open(sys.argv[2], mode='w+') as fw:
        first = 0
        f = 0
        read = fr.readlines()
        for i, line in enumerate(read):
            if "**" in line:
                line = inlineMarkdown(line, "**")
            if "__" in line:
                line = inlineMarkdown(line, "__")
            if "[[" in line and "]]" in line:
                line = md5Markdown(line)
            if "((" in line and "))" in line:
                line = caseMarkdown(line)
            lineSplit = line.split(' ')
            if lineSplit[0] in md:

                if lineSplit[0].startswith('#'):
                    headings(lineSplit[0])

                elif lineSplit[0].startswith("-") or \
                        lineSplit[0].startswith("*"):
                    x = md[lineSplit[0]]

                    if not first:
                        Write = "<{}>\n".format(x)
                        fw.write(Write)
                        first = lineSplit[0]

                    Write = line.replace("{} ".format(lineSplit[0]), "<li>")
                    Write = Write[:-1] + ("</li>\n")
                    fw.write(Write)

                    if i is len(read) - 1 or \
                            not read[i + 1].startswith("{} ".format(first)):
                        Write = "</{}>\n".format(x)
                        fw.write(Write)
                        first = 0
            else:
                if line[0] != "\n":

                    if not f:
                        fw.write("<p>\n")
                        f = 1
                    fw.write(line)

                    if i != len(read) - 1 and read[i + 1][0] != "\n" \
                            and read[i + 1][0] not in md:
                        fw.write("<br/>\n")
                    else:
                        fw.write("</p>\n")
                        f = 0
        exit(0)
        
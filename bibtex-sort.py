# MIT License
#
# Copyright (c) 2019-2020 wolfposd
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sublime
import sublime_plugin


#import logging
#logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
#logging.debug("Starte bibtex-sort")

# sorts by authortag
class BibtexSortCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        oldContent = self.view.substr(sublime.Region(0,self.view.size()))
        newLines = getlines(oldContent)
        newLines = sorted(newLines, key=lambda inStr:inStr[0][inStr[0].index("{"):].lower() )
        outputlines(self, edit, newLines)
        
# sorts by source type (e.g. MISC, INPROCEEDINGS, BOOK, etc) then by author-tag
class BibtexSortTypeCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        oldContent = self.view.substr(sublime.Region(0,self.view.size()))
        newLines = getlines(oldContent)
        newLines = sorted(newLines, key=lambda inStr:inStr[0].lower() )
        outputlines(self, edit, newLines)


# command for sort by author
class BibtexSortAuthorCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        oldContent = self.view.substr(sublime.Region(0,self.view.size()))
        newLines = getlines(oldContent)
        newLines = sorted(newLines, key=lambda ele:findSpecificLine("author=", ele).replace("{{", "{"))
        outputlines(self, edit, newLines)

# command for sort by title
class BibtexSortTitleCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        oldContent = self.view.substr(sublime.Region(0,self.view.size()))
        newLines = getlines(oldContent)
        newLines = sorted(newLines, key=lambda ele:findSpecificLine("title=", ele).replace("{{", "{"))
        outputlines(self, edit, newLines)

#
#
#
# formats all input lines into an array of array for sorting purposes and whatnot
def getlines(input):
        lines = input.splitlines(True)
        newLines = []
        curline = -1

        for line in lines:
            if line.startswith("@"):
                curline += 1
                newLines.append([])

            if len(line.strip(' \r\n\t')) != 0 :
                newLines[curline].append(line)

        return newLines

# outputs the sorted lines into the view
def outputlines(this, edit, output):
    newContent = ""
    for lines in output: 
        for line in lines:
           newContent += line
        newContent += "\n"

    regionAll = sublime.Region(0, this.view.size())
    this.view.replace(edit, regionAll, newContent )

# finds a specific line in [] of elements
def findSpecificLine(linespecifier, element):
    for line in element:
        res = line.replace(" ","").lower()
        if res.find(linespecifier) != -1 :
            return res
    return ""

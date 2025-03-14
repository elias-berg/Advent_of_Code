#!/usr/bin/env python3

# Handy script to create a solution template for Advent of Code.
# You're given the choice of year, day, and language to start with.

#############
# TODO List:
# - Add in language-specific run instructions
# - Add in language-specific file parsing (into a string)
# - Move 'supported_languages' into a JSON file

# To run:
# - python3 create_template.py

import os
import sys
import io
import subprocess

supported_languages = {
  "python": {
    "ext": ".py", 
    "comment": "#",
    "instructions": "- [Install python3](https://www.python.org/downloads/)\n- Run `python3 solution.py`",
    "pre": "#!/usr/bin/env python3\n\n"
  },
  "javascript": {
    "ext": ".js",
    "comment": "//",
    "instructions": ""
  },
  "java": {
    "ext": ".java", 
    "comment": "//",
    "instructions": ""
  },
  "c#": {
    "ext": ".cs", 
    "comment": "//",
    "instructions": ""
  },
  "c": {
    "ext": ".c", 
    "comment": "//",
    "instructions": ""
  },
  "clojure": {
    "ext": ".clj",
    "comment": ";;",
    "instructions": "- [Install Clojure](https://clojure.org/guides/install_clojure)\n- Run `clj solution.clj",
    "pre": "(ns solution\n  (:require [clojure.string :as str]))\n\n",
    "post": "(defn main []\n  (let [input (slurp \"input.txt\")]))\n\n(main)\n"
  },
  "go": {
    "ext": ".go",
    "comment": "//",
    "instructions": "",
    "post": "package main\n\nimport (\n	\"fmt\"\n	\"os\"\n)\n\nfunc main() {\ndata, error := os.ReadFile(\"input.txt\")\n  if error != nil {\n    fmt.Println(error.Error())\n    return\n  }\n}"
  }
}

#TODO: Add in boilerplate code to parse the input and args

##############
# Script Start

cwd = os.getcwd()
if str.find(cwd, "Advent_of_Code") == -1:
  print("Run the script from the root directory!")

# TODO: Support command line args
if len(sys.argv) != 1:
  print("Multiple arguments not supported at this time.")

print("==== Create Solution Template ====")
print("Enter \"quit\" to leave the program at any point.\n")

############################################################
# Get the AoC year, day, and language to create the template

# Helper function to continually prompt the user for a value until they
# enter something within the list of options.
def getInput(prompt, options):
  value = input(prompt)
  if value != "quit":
    while value not in options:
      value = input(prompt)
      if value == "quit":
        sys.exit(0)
  if value == "quit":
    sys.exit(0)
  
  return value

# Year

yearAry = list(map(str, range(2015, 2025)))
year = getInput("What year?\n(" + ", ".join(yearAry) + ")\n", yearAry)

# Day

dayAry = list(map(str, range(1, 26)))
day = getInput("What day?\n(" + ", ".join(dayAry) + ")\n", dayAry)

# Language

langAry = []
for key in supported_languages.keys():
  langAry.append(key)
if year != "2024":
  lang = getInput("What language?\n(" + ", ".join(langAry) + ")\n", langAry)

########################
# Create the directories

if year not in os.listdir():
  os.mkdir(year)
os.chdir(year)

if year == "2024":
  day = "day" + day

if day in os.listdir():
  print("A solution directory already exists for " + year + " day " + day + ".")
  sys.exit(0)
else:
  os.mkdir(day)
  os.chdir(day)
  
  # Special treatment for 2024 - Django app
  if year == "2024":
    file = io.open("solution.py", "w")
    file.write("from template.Solution import Solution\n\n" +
                "class Day" + day[3:] + "Solution(Solution):\n" +
                "  def __init__(self):\n" +
                "    super().__init__(" + day[3:] + ")\n" +
                "    self.part1 = True\n\n" +
                "  def Part1(self):\n" +
                "    input = self.readInput()\n" +
                "    return 0\n\n" +
                "  pass\n\n" +
                "urlpatterns = Day" + day[3:] + "Solution().urls()")
    file.close()


#########################
# Get the current problem

p = subprocess.Popen(["curl", "https://adventofcode.com/" + year + "/day/" + day, "-s"],
  stdout=subprocess.PIPE,
  shell=False)
p.wait() # Race condition...
html = str(p.stdout.read())
# Assumption here that the problem name is always surrounded by "---"
nameStartStr = "Day " + day + ": "
nameLoc = [html.find(nameStartStr), html.find(" ---")]
problemName = html[nameLoc[0] + len(nameStartStr):nameLoc[1]]
print("--> Loaded day: \"" + problemName + "\"") # Print the name for display

#TODO: Parse the sample input and create "sample_input.txt"

############################################
# Generate the README and code template file

if year != "2024":
  template = supported_languages[lang]
  comment = template["comment"]
  codeFileName = "solution" + template["ext"]

  # Write the standard README
  readme = io.open("README.md", "w")
  readme.writelines(
    ["# [Advent of Code " + year + " - Day " + day + "](https://adventofcode.com/" + year + "/day/" + day + ") - " + problemName + "\n",
    "\n",
    "### [" + codeFileName + "](./" + codeFileName + ")\n",
    template["instructions"] + "\n",
    "\n",
    "### Performance\n",
    "\n",
    "| Part | Time |\n",
    "| ---: | ---: |\n"
    "|    1 |      |\n",
    "|    2 |      |\n"])
  readme.close()

  # Write the code file stub
  # Add any additional header info if the language uses it,
  # e.g. the python usr/bin line to run the file as a script
  code = io.open(codeFileName, "w")
  if "pre" in template:
    code.write(template["pre"])
  # Add any post-summary info, like run instructions
  if "post" in template:
    code.write(template["post"])
  code.close()

# Just create blank input files
io.open("input.txt", "w").close()
io.open("sample_input.txt", "w").close()

print("\n== DONE ==\n")

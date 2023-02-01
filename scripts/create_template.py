#!/usr/bin/env python3

# Handy script to create a solution template for Advent of Code.
# You're given the choice of year, day, and language to start with.

#############
# To-do List:
# - Add in language-specific run instructions
# - Add in language-specific file parsing (into a string)
# - Create a README per directory?

# To run:
# - python3 create_template.py

import os
import sys
import io
import subprocess

supported_languages = {
  "python":     {"ext": ".py", 
                "comment": "#",
                "addl": "#!/usr/bin/env python3\n\n"},
  "javascript": {"ext": ".js", 
                "comment": "//"},
  "java":       {"ext": ".java", 
                "comment": "//"},
  "c#":         {"ext": ".cs", 
                "comment": "//"},
  "c":          {"ext": ".c", 
                "comment": "//"},
  "clojure":    {"ext": ".clj",
                "comment": ";;"}
}

##############
# Script Start

cwd = os.getcwd()
if str.find(cwd, "Advent_of_Code") == -1:
  print("Run the script from the root directory!")

# Look for the input
if len(sys.argv) != 1:
  print("Multiple arguments not supported at this time.")

print("==== Create Solution Template ====")
print("Enter \"quit\" to leave the program at any point.\n")

########################################
# Get the AoC year, day, and language to
# create the template for

yearAry = list(map(str, range(2015, 2023)))
yearPrompt = "What year?\n(" + ", ".join(yearAry) + ")\n"
year = input(yearPrompt)
if year != "quit":
  while year not in yearAry:
    year = input(yearPrompt)
    if year == "quit":
      sys.exit(0)
if year == "quit":
  sys.exit(0)

dayAry = list(map(str, range(1, 26)))
dayPrompt = "What day?\n(" + ", ".join(dayAry) + ")\n"
day = input(dayPrompt)
if day != "quit":
  while day not in dayAry:
    day = input(dayPrompt)
    if day == "quit":
      sys.exit(0)
if day == "quit":
  sys.exit(0)

langAry = []
for key in supported_languages.keys():
  langAry.append(key)
langPrompt = "What language?\n(" + ", ".join(langAry) + ")\n"
lang = input(langPrompt)
if lang != "quit":
  while lang not in langAry:
    lang = input(langPrompt)
    if lang == "quit":
      sys.exit(0)
if lang == "quit":
  sys.exit(0)

########################
# Create the directories

if year not in os.listdir():
  os.mkdir(year)
os.chdir(year)

if day in os.listdir():
  print("A solution directory already exists for " + year + " day " + day + ".")
  sys.exit(0)
os.mkdir(day)
os.chdir(day)

#########################
# Get the current problem

p = subprocess.Popen(["curl", "https://adventofcode.com/" + year + "/day/" + day],
  stdout=subprocess.PIPE,
  shell=False)
html = str(p.stdout.read())
# Assumption here that the problem name is always surrounded by "---"
nameStartStr = "Day " + day + ": "
nameLoc = [html.find(nameStartStr), html.find(" ---")]
problemName = html[nameLoc[0] + len(nameStartStr):nameLoc[1]]

##############################
# Now create the template file

comment = supported_languages[lang]["comment"]
file = io.open("solution" + supported_languages[lang]["ext"], "w")
# Add any additional header info if the language uses it,
# e.g. the python usr/bin line to run the file as a script
if "add" in supported_languages[lang]:
  file.write(supported_languages[lang]["addl"])
# Write the standard template
file.writelines(
  [comment + " Advent of Code " + year + " Day " + day + "\n",
   comment + " " + problemName + "\n",
   comment + "\n",
   comment + " <Problem Statement>\n",
   comment + "\n",
   comment + " Part 1 -\n",
   comment + "\n"])
file.close()

# Input file
if "SESSION" in os.environ:
  sessionID = os.environ["SESSION"] # Pull it from an environment variable
  if len(sessionID) > 0:
    subprocess.call([
      "curl",
      "https://adventofcode.com/" + year + "/day/" + day + "/input",
      "--cookie",
      "session=" + sessionID,
      "-o",
      "input.txt"
    ])
else:
  print("\nTo download specific problem inputs, add your Advent of Code" \
  "\"session\" cookie as an environment variable.\n")

print("\n== DONE ==\n")

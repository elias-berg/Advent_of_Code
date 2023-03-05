#!/usr/bin/env python3

# Handy script to create a solution template for Advent of Code.
# You're given the choice of year, day, and language to start with.

#############
# TODO List:
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
                 "pre": "#!/usr/bin/env python3\n\n"},
  "javascript": {"ext": ".js", 
                 "comment": "//"},
  "java":       {"ext": ".java", 
                 "comment": "//"},
  "c#":         {"ext": ".cs", 
                 "comment": "//"},
  "c":          {"ext": ".c", 
                 "comment": "//"},
  "clojure":    {"ext": ".clj",
                 "comment": ";;"},
  "go":         {"ext": ".go",
                 "comment": "//",
                 "post": "\npackage main\n\nfunc main() {\n}"}
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

########################################
# Get the AoC year, day, and language to
# create the template for

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

yearAry = list(map(str, range(2015, 2023)))
year = getInput("What year?\n(" + ", ".join(yearAry) + ")\n", yearAry)

# Day

dayAry = list(map(str, range(1, 26)))
day = getInput("What day?\n(" + ", ".join(dayAry) + ")\n", dayAry)

# Language

langAry = []
for key in supported_languages.keys():
  langAry.append(key)
lang = getInput("What language?\n(" + ", ".join(langAry) + ")\n", langAry)

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

##############################
# Now create the template file

comment = supported_languages[lang]["comment"]
file = io.open("solution" + supported_languages[lang]["ext"], "w")
# Add any additional header info if the language uses it,
# e.g. the python usr/bin line to run the file as a script
if "pre" in supported_languages[lang]:
  file.write(supported_languages[lang]["pre"])
# Write the standard template
file.writelines(
  [comment + " Advent of Code " + year + " - Day " + day + "\n",
   comment + " " + problemName + "\n",
   comment + "\n",
   comment + " <Problem Statement>\n",
   comment + "\n",
   comment + " Part 1 -\n",
   comment + "\n"])
# Add any post-summary info, like run instructions
if "post" in supported_languages[lang]:
  file.write(supported_languages[lang]["post"])

file.close()

# Input file
if "SESSION" in os.environ and len(os.environ["SESSION"]) > 0:
  sessionID = os.environ["SESSION"] # Pull it from an environment variable
  if len(sessionID) > 0:
    subprocess.call([
      "curl",
      "https://adventofcode.com/" + year + "/day/" + day + "/input",
      "--cookie",
      "session=" + sessionID,
      "-o",
      "input.txt",
      "-s",
      "-w",
      "--> Downloaded input.txt"
    ])
else:
  print("\nTo download specific problem inputs, add your Advent of Code " \
  "\"session\" cookie as an environment variable.\n")

print("\n== DONE ==\n")

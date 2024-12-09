# Advent of Code

## Summary

For-fun repository filled with Eli's attempts at solving [Advent of Code](www.adventofcode.com) problems.

### 2024

This year, in honor of joining Klaviyo, I wanted to brush up on my Python and incorporate Django. The year is a single django project where each day is a separate app. Each app then has two primary endpoints, for part 1 and part 2.

The Makefile at the root can kick off the web server at `localhost:8000` via
```shell
make 2024
```

#### To Do
- Create a view to query each day and part.
- Add a parameter to the request body to use the sample input.
- Make a generic class to represent a day.
- Auto-generate the links in the view.
- Possibly make each day have its own view to show performance?

### 2022

To approach each problem, I try to use a different language, though not necessarily the best language suited to the task at hand. This is more to practice with multiple languages. For example, [2022 Day 15's solution](./2022/15/solution.clj) made me seriously regret using Clojure as it would have been significantly easier with a language like Python.

Each solution file contains two main parts:
- File reading and parsing, "input.txt"
- The solution to the problem at hand

Also, note that the solution directories also provide "sample_input.txt". This is the input provided by the problem on the Advent of Code site, used for testing solutions.

| Day  | Name                                 | Language   | Day  | Name                                  | Language   |
| ---- | ------------------------------------ | ---------- | ---- | ------------------------------------- | ---------- |
| *1*  | [Calorie Counting](./2022/1)         | Clojure    | *14* | [Regolith Reservoir](./2022/14)       | Node.js    |
| *2*  | [Rock, Paper, Scissors](./2022/2)    | Python     | *15* | [Beacon Exclusion Zone](./2022/15)    | Clojure    |
| *3*  | [Rucksack Reorganization](./2022/3)  | Javascript | *16* | [Proboscidea Volcanium](./2022/16)    | C#         |
| *4*  | [Camp Cleanup](./2022/4)             | Java       | *17* | [Pyroclastic Flow](./2022/17)         | Typescript |
| *5*  | [Supply Stacks](./2022/5)            | Javascript | *18* | [Boiling Boulders](./2022/18)         | Python     |
| *6*  | [Tuning Trouble](./2022/6)           | M          | *19* | [Not Enough Minerals](./2022/19)      | Go         |
| *7*  | [No Space Left On Device](./2022/7)  | Clojure    | *20* | [Grove Positioning System](./2022/20) | Java       |
| *8*  | [Treetop Tree House](./2022/8)       | Python     | *21* | [Monkey Math](./2022/21)              | Javascript |
| *9*  | [Rope Bridge](./2022/9)              | C#         | *22* | [Monkey Map](./2022/22)               | C++        |
| *10* | [Cathode-Ray Tube](./2022/10)        | C          | *23* | [Unstable Diffusion](./2022/23)       | C#         |
| *11* | [Monkey in the Middle](./2022/11)    | Java       | *24* | [Blizzard Basin](./2022/24)           | Go         |
| *12* | [Hill Climbing Algorithm](./2022/12) | Go         | *25* | [Full of Hot Air](./2022/25)          | Clojure    |
| *13* | [Distress Signal](./2022/13)         | Python     |

### 2021

I actually started this year after I completed 2022, so it's continuation of the pattern of using any language I felt like for each problem.

| Day  | Name                                 | Language   |
| ---- | ------------------------------------ | ---------- |
| *1*  | [Sonar Sweep](./2021/1)              | Clojure    |
| *2*  | [Dive!](./2021/2)                    | Go         |
| *3*  | [Binary Diagnostic](./2021/3)        | Python     |
| *4*  | [Giant Squid](./2021/4)              | C#         |
| *5*  | [Hydrothermal Vents](./2021/5)       | Rust       |

### Scripts

There's also a scripts directory that provides the following script(s) and how to run them:

`python3 ./scripts/create_template.py`

**Important Note:** This script is only meant for 2022 and 2021. It doesn't (yet?) have special handling for 2024 where days are new django apps.

*Creates a template for the year and day of the problem to solve and language I'll try to use.*
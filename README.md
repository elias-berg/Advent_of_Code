# Advent of Code

## Summary

For-fun repository filled with Eli's attempts at solving [Advent of Code](www.adventofcode.com) problems.

To approach each problem, I try to use a different language, though not necessarily the best language suited to the task at hand. This is more to practice with multiple languages. For example, [2022 Day 15's solution](./2022/15/solution.clj) made me seriously regret using Clojure as it would have been significantly easier with a language like Python.

Each solution file contains two main parts:
- File reading and parsing, "input.txt"
- The solution to the problem at hand

Also, note that the solution directories also provide "sample_input.txt". This is the input provided by the problem on the Advent of Code site, used for testing solutions.

### 2022

| Day  | Name                                 | Lang.      | Day  | Name                                  | Lang.      |
| ---- | ------------------------------------ | ---------- | ---- | ------------------------------------- | ---------- |
| *1*  | [Calorie Counting](./2022/1)         | Clojure    | *14* | [Regolith Reservoir](./2022/14)       | Node.js    |
| *2*  | [Rock Paper Scissors](./2022/2)      | Python     | *15* | [Beacon Exclusion Zone](./2022/15)    | Clojure    |
| *3*  | [Rucksack Reorganization](./2022/3)  | Javascript | *16* | [Proboscidea Volcanium](./2022/16)    | C#         |
| *4*  | [Camp Cleanup](./2022/4)             | Java       | *17* | [Pyroclastic Flow](./2022/17)         | Typescript |
| *5*  | [Supply Stacks](./2022/5)            | Javascript | *18* | [Boiling Boulders](./2022/18)         | Python     |
| *6*  | [Tuning Trouble](./2022/6)           | M          | *19* | [Not Enough Minerals](./2022/19)      | Go         |
| *7*  | [No Space Left On Device](./2022/7)  | Clojure    | *20* | [Grove Positioning System](./2022/20) | Java       |
| *8*  | [Treetop Tree House](./2022/8)       | Python     | *21* | [Monkey Math](./2022/21)              | Javascript |
| *9*  | [Rope Bridge](./2022/9)              | C#         |
| *10* | [Cathode-Ray Tube](./2022/10)        | C          |
| *11* | [Monkey in the Middle](./2022/11)    | Java       |
| *12* | [Hill Climbing Algorithm](./2022/12) | Go         |
| *13* | [Distress Signal](./2022/13)         | Python     |

### Scripts

There's also a scripts directory that provides the following scripts and how to run them:

`python3 ./scripts/create_template.py`

*Creates a template for the year, day, and language I plan on using.*
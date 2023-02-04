// Advent of Code 2022 - Day 21
// Monkey Math
//
// You re-encounter the monkeys who are either yelling a specific
// number or a result of a math operation. The monkeys yelling a
// math operation are actually yelling the names of other monkeys
// of whom they're waiting for their values. The monkeys will keep
// yelling until their value is determined, all the way until the
// monkey named "root" figures out what his value is.
//
// Part 1 -
// What number will "root" yell?
//
// Part 2 -
// There was a translation error. Apparently the operation yelled
// by the "root" monkey was an equality operation. Turns out that
// you're supposed to be the "humn" monkey and need to yell the
// number that will cause the "root" monkey's equality be true.
// What number does "humn" need to yell?

// To run:
// - "node solution.js"

const fs = require('fs');

class Monkey {
  // Parse out a string into a Number or Operation monkey
  constructor(monkey) {
    let info = monkey.split(": ");

    this.Name = info[0];

    let operation = info[1].split(" ");
    if (operation.length == 1) {
      this.Number = parseInt(operation[0]);
    } else {
      // There's an assumption that operation monkeys only mention two
      // other monkeys plus a math operation.
      this.Left = operation[0];
      this.Op = operation[1];
      this.Right = operation[2];
      this.OtherMonkeys = [this.Left, this.Right];
    }
  }
  
  // Helper function to set the value of a monkey based on it's Left
  // and Right values. Will only set the Number once the Left and Right
  // are satisfied.
  SetOtherMonkeyValue = (monkey) => {
    let name = monkey.Name;
    if (name == this.Left) {
      this.Left = monkey.Number;
      this.CurValue = parseInt(this.Left); // Set the "current value" for Part 2
    } else if (name == this.Right) {
      this.Right = monkey.Number;
      this.CurValue = parseInt(this.Right); // Set the "current value" for Part 2
    }
    
    this.OtherMonkeys = this.OtherMonkeys.filter(x => x !== name);

    // If Left and Right are set, then tell the caller that this is
    // now a Number monkey!
    if (this.OtherMonkeys.length === 0) {
      let evalStr = this.Left + this.Op + this.Right;
      this.Number = parseInt(eval(evalStr)); // Might be minimally faster if we remove 'eval'
      return true;
    }
    return false;
  }
}

// Here we know that another monkey references this monkey and
// we should set one of the Left/Right values.
let recursiveSet = (monkeyDict, refDict, numMonkey) => {
  let dependents = refDict[numMonkey.Name];
  if (!dependents) {
    return;
  }
  // Go through each monkey dependent on the number monkey and try to set it's value
  for (let monkeyName of dependents) {
    let monkey = monkeyDict[monkeyName];
    if (monkey.SetOtherMonkeyValue(numMonkey)) {
      recursiveSet(monkeyDict, refDict, monkey);
    }
  }
}

// Given the monkey and dependency dictionaries, see if we can pull any
// dependency values out of what may already be in the dictionary.
let trySetMonkey = (monkeyDict, refDict, monkey, dependencyName) => {
  // See if the dependency has been seen before...
  let dependency = monkeyDict[dependencyName];
  if (dependency && dependency.Number) {
    // We've seen the dependency monkey, so 
    if (monkey.SetOtherMonkeyValue(dependency)) {
      recursiveSet(monkeyDict, refDict, monkey);
    }
  } else {
    // Not found; list it in the dependency directory
    if (!refDict[dependencyName]) {
      refDict[dependencyName] = [];
    }
    refDict[dependencyName].push(monkey.Name);
  }
}

// Main solution code for Part 1:
// Uses a dictionary reference to all the monkeys as well as a dependency dictionary
// to evaluate dependencies as they come up.
let part1 = (monkeys) => {
  let monkeyDict = {}; // Monkey name -> Monkey
  let refDict = {}; // Monkey depended on name -> dictionary of dependent monkeys

  let root = undefined;
  for (let monkey of monkeys) {
    let cur = new Monkey(monkey);
    let name = cur.Name;

    if (name === "root") {
      root = cur;
    }

    // Always add the current monkey and who it references to the dictionaries
    monkeyDict[name] = cur;

    // If this is a number monkey, we want to first see if there are any other monkeys
    // that need this number
    if (cur.Number) {
      recursiveSet(monkeyDict, refDict, cur);
    } else {
      trySetMonkey(monkeyDict, refDict, cur, cur.Left);
      trySetMonkey(monkeyDict, refDict, cur, cur.Right);
    }
  }

  return root.Number;
}

// Solve for X given the operation, Y value, current value,
// and what side of the operand X is on (only matters for - and /).
let solveForX = (xIsRight, op, y, val) => {
  if (op === "+") {
    return (val - y);
  } else if (op === "-") {
    if (xIsRight) { // x is right of the op
      return -1 * (val - y);
    } else { // x is left of the op
      return val + y;
    }
  } else if (op === "*") {
    return val / y;
  } else if (op === "/") {
    if (xIsRight) {
      return y / val;
    } else { // Left is always easier
      return val * y;
    }
  }
  // If anything else...that would be wack
}

// Recursive function to apply the OPPOSITE operation to the current value
// in order to solve for "humn"
let recursiveSolve = (mDict, monkey, curValue) => {
  // Useful debug print
  //console.log(monkey.Name + " -> " + monkey.Left + " " + monkey.Op + " " + monkey.Right + " = " + curValue);

  // Base case: we reach humn
  if (monkey.Name === "humn") {
    monkey.Number = curValue;
  } else {
    // First get the next unknown monkey. Note that we need the right/left side
    // determined for the math operation
    let unknownName = monkey.OtherMonkeys[0];
    let xIsRight = unknownName === monkey.Right;
    // curValue = # <op> ? --> curValue <opposite of op> # = ?
    let newValue = solveForX(xIsRight, monkey.Op, monkey.CurValue, curValue);

    recursiveSolve(mDict, mDict[unknownName], newValue)
  }
}

// The plan is to solve the entire tree, except for everything from humn up to root
let part2 = (monkeys) => {
  let monkeyDict = {}; // Monkey name -> Monkey
  let refDict = {}; // Monkey depended on name -> dictionary of dependent monkeys

  let root = undefined;
  let humn = undefined;

  for (let monkey of monkeys) {
    let cur = new Monkey(monkey);
    let name = cur.Name;

    if (name === "root") {
      root = cur;
    }
    if (name === "humn") {
      humn = cur;
      continue;
    }

    // This time around, we DON'T want to add it for any other monkey to reference
    monkeyDict[name] = cur;

    // If this is a number monkey, we want to first see if there are any other monkeys
    // that need this number
    if (cur.Number) {
      recursiveSet(monkeyDict, refDict, cur);
    } else { // Force "humn" to not get evaluated
      trySetMonkey(monkeyDict, refDict, cur, cur.Left);
      trySetMonkey(monkeyDict, refDict, cur, cur.Right);
    }
  }

  // Now add humn to the dictionary
  monkeyDict[humn.Name] = humn;

  // Now, let's start at "root" and work our way all the way back down to "humn"
  recursiveSolve(monkeyDict, monkeyDict[root.OtherMonkeys[0]], root.CurValue)

  return humn.Number;
}

///////////////
// Start Script

var fileName = "input.txt";
if (process.argv.length == 3 && process.argv[2] == "-sample") {
  fileName = "sample_input.txt";
}

fs.readFile(fileName, (err, data) => {
  if (err) throw err; // Unexpected, but expect it anyway
  
  let monkeys = data.toString().split("\n");

  let start = Date.now();
  let val = part1(monkeys);
  let endPart1 = Date.now();
  console.log("Part 1: " + val + " (Ran in " + (endPart1 - start) + "ms)");

  val = part2(monkeys);
  let endPart2 = Date.now();
  console.log("Part 2: " + val + " (Ran in " + (endPart2 - endPart1) + "ms)");
});
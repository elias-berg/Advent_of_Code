// Advent of Code 2022 - Day 17
// Pyroclastic Flow
//
// The handheld device located an alternative exit from the cave.
// Pursuing this exit, you come to a very tall, narrow chamber where
// large rocks are falling into the chamber from above. You have to
// determine where the rocks will fall or you'll get crushed!
//
// There are five types of rocks that will fall in order:
// Horizontal, Plus-shaped, Backwards-L, Vertical, and Square
//
// The input is a series of jet stream movements that push the rocks
// either to the left or right.
// Each movement sequence goes:
// 1) Shift in the direction of the jet stream
// 2) Move the rock down one
//
// If a rock can't shift, then it doesnt. If a rock can't move down any further
// it gets added to the tower.
//
// Part 1 -
// Given the jet stream input and that each rock's bottom is 3 positions
// from the top of the tower and left is 2 positions from the left of the
// tunnel, what will be the height of the tower after 2022 blocks have fallen?
//
// Part 2 -
// The elephants aren't satisfied with the simulation and want to know the
// height of the tower after 1,000,000,000,000 (one trillion) rocks have fallen...

// To run:
// - First, you'll need to navigate to the /17 directory.
// - Make sure you have node installed and run 'npm install' from the /17 directory.
// - Once everything is installed, run 'npm run start'.
// - In a browser, navigate to 'localhost:8080'.
// - You'll see the main page where you can then click the buttons to run the
//   sample input or run using the main input.

import BlockSimulation from './Simulation.js';

let Simulation: BlockSimulation;
let PartOne = false;

/***************
 * UI Functions
 ***************/

// First, register handlers on all the buttons
$("#pick1").on("click", () => Pick(true));
$("#pick2").on("click", () => Pick(false));
$("#load1").on("click", () => Load("sample_input.txt"));
$("#load2").on("click", () => Load("input.txt"));
$("#run1").on("click", () => Start(false));
$("#run2").on("click", () => Start(true));
$("#reset").on("click", () => Reset());

// Sets the "part" we want to run (i.e. Part 1 or Part 2)
const Pick = (partOne: boolean) => {
  PartOne = partOne;
  if (partOne) {
    $("#pick1").attr("data-type", "picked");
  } else {
    $("#pick2").attr("data-type", "picked");
  }

  $("#pick1").prop("disabled", true);
  $("#pick2").prop("disabled", true);
  $("#load1").prop("disabled", false);
  $("#load2").prop("disabled", false);
}

// Helper function to load a specific file from the front-end
const Load = (file: string) => {
  if (file === "sample_input.txt") {
    $("#load1").attr("data-type", "picked");
  } else {
    $("#load2").attr("data-type", "picked");
  }

  $("#load1").prop("disabled", true);
  $("#load2").prop("disabled", true);
  $("#run1").prop("disabled", false);
  $("#run2").prop("disabled", false);

  fetch(file)
    .then((res) => res.text()
      .then((text) => {
        Simulation = new BlockSimulation(text, $("#tower"), PartOne);
        Simulation.BlockCountElement = $("#blockCounter");
        Simulation.TowerHeightElement = $("#heightCounter");
      }));
}

// Call-in from the front-end, wrapper for the main function.
const Start = (fastMode: boolean) => {
  if (!fastMode) {
    $("#run1").attr("data-type", "picked");
  } else {
    $("#run2").attr("data-type", "picked");
  }

  $("#run1").prop("disabled", true);
  $("#run2").prop("disabled", true);

  setTimeout(() => Simulation.MoveBlocks(fastMode), 0);
}

// Resets the state of the application
const Reset = () => {
  // Clean up UI
  $("#pick1").prop("disabled", false);
  $("#pick1").attr("data-type", "");
  $("#pick2").prop("disabled", false);
  $("#pick2").attr("data-type", "");
  $("#load1").prop("disabled", true);
  $("#load1").attr("data-type", "");
  $("#load2").prop("disabled", true);
  $("#load2").attr("data-type", "");
  $("#run1").prop("disabled", true);
  $("#run1").attr("data-type", "");
  $("#run2").prop("disabled", true);
  $("#run2").attr("data-type", "");

  $("#blockCounter").text("0");
  $("#heightCounter").text("0");

  $("#tower").empty();

  Simulation.Reset();

  // Reset globals
  PartOne = false;
}
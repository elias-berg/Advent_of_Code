// You meet back up with the elves where the starfruit grove is supposed to
// be! But...there's no starfruit, so the elves elect to plant seeds in the
// grove. They're frantic and decide to bustle around like so:
// - Each turn, each elf considers the same direction first to move.
// - The order of directions goes N, S, W, E.
// - If no elves are in any of a direction's spaces adjacent, then the
//   elf proposes to move directly in that direction.
// - If a direction doesn't work, they consider the next direction.
// - If all directions work, then the elf doesn't move, as well as if
//   no directions work, the elf won't move.
// - If two elves propose the same spot, then no elves move.
// - At the end of the turn, the turn's considered direction moves to
//   the end of the list and the next direction is considered first next turn.
//
// Part 1 -
// After 10 turns, how many empty spaces are there in the grove, given the
// grove is a rectangle perfectly encapsulating all of the elves?
//
// Part 2 -
// What is the first turn number where no elves move?

using System;
using System.Diagnostics;
using System.Collections.Generic;

public class Elf {
  public static char[] Directions = {'N', 'S', 'W', 'E'};
  public static int DirectionIdx = 0;
  public static Dictionary<string, Elf> Moves;
  public static Dictionary<string, Elf> Elves;

  static Elf() {
    Moves = new Dictionary<string, Elf>();
    Elves = new Dictionary<string, Elf>();
  }

  public int X;
  public int Y;
  private int NextX;
  private int NextY;
  public string NextKey;

  public Elf(int x, int y) {
    X = x;
    Y = y;
    NextKey = "";
    Elf.Elves.Add(x + "," + y, this);
  }

  private bool Check(char dir) {
    if (dir == 'N') {
      return
        !Elf.Elves.ContainsKey((X-1) + "," + (Y-1)) &&
        !Elf.Elves.ContainsKey(X + "," + (Y-1)) &&
        !Elf.Elves.ContainsKey((X+1) + "," + (Y-1));
    } else if (dir == 'S') {
      return
        !Elf.Elves.ContainsKey((X-1) + "," + (Y+1)) &&
        !Elf.Elves.ContainsKey(X + "," + (Y+1)) &&
        !Elf.Elves.ContainsKey((X+1) + "," + (Y+1));
    } else if (dir == 'W') {
      return
        !Elf.Elves.ContainsKey((X-1) + "," + (Y-1)) &&
        !Elf.Elves.ContainsKey((X-1) + "," + Y) &&
        !Elf.Elves.ContainsKey((X-1) + "," + (Y+1));
    } else { // dir == 'E'
      return
        !Elf.Elves.ContainsKey((X+1) + "," + (Y-1)) &&
        !Elf.Elves.ContainsKey((X+1) + "," + Y) &&
        !Elf.Elves.ContainsKey((X+1) + "," + (Y+1));
    }
  }

  public void DetermineMove() {
    NextKey = "";

    char? goDir = null;
    bool allDirs = true;
    for (int i = 0; i < Elf.Directions.Length; i++) {
      int dirIdx = (Elf.DirectionIdx + i) % Elf.Directions.Length;
      bool curDir = Check(Elf.Directions[dirIdx]);
      allDirs = allDirs && curDir; // Keep track of if the elf is totally alone
      // Only actually set the FIRST proposed direction, but we need to see if the elf is solo still 
      if (curDir && goDir == null) {
        goDir = Elf.Directions[dirIdx];
      }
    }

    // If no directions were valid or if the elf is isolated, then don't move
    if (goDir == null || allDirs) {
      return;
    }

    NextX = X;
    NextY = Y;
    if (goDir == 'N') {
      NextY--;
    } else if (goDir == 'S') {
      NextY++;
    } else if (goDir == 'W') {
      NextX--;
    } else { // goDir == 'E'
      NextX++;
    }

    NextKey = NextX + "," + NextY;
    if (!Elf.Moves.ContainsKey(NextKey)) {
      Elf.Moves.Add(NextKey, this);
    } else { // If some other elf wants to move to the same spot, then cancel both
      Elf.Moves[NextKey] = null;
      NextKey = "";
    }
  }

  /**
   * Wrapper around the Moves dictionary to move all of the elves
   */
  public static bool MoveElves() {
    bool moved = false;
    foreach (string key in Elf.Moves.Keys) {
      Elf e = Elf.Moves[key];
      if (e != null) {
        moved = true;
        e.Move();
      }
    }

    Elf.DirectionIdx++;
    Elf.DirectionIdx = Elf.DirectionIdx % Elf.Directions.Length;
    Elf.Moves.Clear();

    return moved;
  }

  private void Move() {
    Elf.Elves.Remove(X + "," + Y);
    Elf.Elves.Add(NextKey, this);
    X = NextX;
    Y = NextY;
    NextKey = ""; // Clear for the next iteration
  }
}

public class solution {
  public static void Main(string[] args) {
    // Step 0: which input file?
    string inputFile = "input.txt";
    if (args.Length == 1 && args[0] == "-sample") {
      inputFile = "sample_input.txt";
    }

    Stopwatch timer = new Stopwatch();
    timer.Start();

    // Step 1: parse the input
    List<Elf> elves = new List<Elf>();
    string[] lines = System.IO.File.ReadAllLines(inputFile);
    int y = 0;
    foreach (string line in lines) {
      int x = 0;
      foreach (char space in line) {
        if (space == '#') {
          Elf e = new Elf(x, y);
          elves.Add(e);
        }
        x++; // X increases with each character
      }
      y++; // Y increases with each line
    }

    // Step 2: move elves around the grid for part 1
    int moveNum = 0;
    bool oneMoved = true;
    for (int i = 0; i < 10; i++) {
      foreach (Elf e in elves) {
        e.DetermineMove();
      }
      oneMoved = Elf.MoveElves();
      if (oneMoved) {
        moveNum++;
      }
    }

    // Step 3: detemine the max size of the grid!
    int xMin = 0, xMax = 0, yMin = 0, yMax = 0;
    foreach (Elf e in elves) {
      xMin = Math.Min(e.X, xMin);
      xMax = Math.Max(e.X, xMax);
      yMin = Math.Min(e.Y, yMin);
      yMax = Math.Max(e.Y, yMax);
    }
    int w = (xMax - xMin) + 1; // Don't forget to account for 0!
    int h = (yMax - yMin) + 1;
    timer.Stop();
    System.Console.WriteLine("Part 1: " + ((w * h) - elves.Count) + " (" + timer.Elapsed.Milliseconds + "ms)");

    // Step 4: continue moving elves around the grid for part 2
    timer.Start();
    while (oneMoved) {
      oneMoved = false; // Set to false for each iteration
      foreach (Elf e in elves) {
        e.DetermineMove();
      }
      if (Elf.MoveElves()) {
        oneMoved = true;
      }
      moveNum++; // Because we need the first turn that NO elves moved
    }
    timer.Stop();
    System.Console.WriteLine("Part 2: " + moveNum + " (" + timer.Elapsed.Milliseconds + "ms)");
  }
}
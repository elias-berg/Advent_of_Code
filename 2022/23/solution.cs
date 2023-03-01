// Advent of Code 2022 - Day 23
// Unstable Diffusion
//
// <Problem Statement>
//
// Part 1 -
//

// To run:
// I used .NET 7.0 x64 for macOS and Mono (https://www.mono-project.com/)
// - Use the command 'csc solution.cs' to compile
// - Then use 'mono solution.exe' to run

using System;
using System.Collections.Generic;

public class Elf {
  public static char[] Directions = {'N', 'S', 'W', 'E'};
  public static int DirectionIdx = 0;
  public static Dictionary<string, bool> Moves;
  public static Dictionary<string, Elf> Elves;

  static Elf() {
    Moves = new Dictionary<string, bool>();
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
      Elf.Moves.Add(NextKey, true);
    } else { // If some other elf wants to move to the same spot, then cancel both
      Elf.Moves[NextKey] = false;
      NextKey = "";
    }
  }

  public void Move() {
    if (NextKey != "" && Elf.Moves[NextKey] == true) {
      Elf.Elves.Remove(X + "," + Y);
      Elf.Elves.Add(NextKey, this);
      X = NextX; // Null-coalesce for the compiler
      Y = NextY;
    }
    NextKey = ""; // Clear for the next iteration
  }

  public static void EndRound() {
    Elf.DirectionIdx++;
    Elf.DirectionIdx = Elf.DirectionIdx % Elf.Directions.Length;
    Elf.Moves.Clear();
  }
}

public class solution {

  public static void Main(string[] args) {
    // Step 0: which input file?
    string inputFile = "input.txt";
    if (args.Length == 1 && args[0] == "-sample") {
      inputFile = "sample_input.txt";
    }

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

    // Step 2: moves elves around the grid for part 1
    for (int i = 0; i < 10; i++) {
      foreach (Elf e in elves) {
        e.DetermineMove();
      }
      foreach (Elf e in elves) {
        e.Move();
      }
      Elf.EndRound();
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
    System.Console.WriteLine("Part 1: " + ((w * h) - elves.Count));
  }
}
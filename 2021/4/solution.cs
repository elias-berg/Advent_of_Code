using System;
using System.Diagnostics;
using System.Collections.Generic;

public class Point {
  public readonly int r;
  public readonly int c;
  public Point(int r, int c) {
    this.r = r;
    this.c = c;
  }
}

public class Board
{
  private string[][] _nums;
  private Dictionary<string, Point> _numMap;
  public Board(string[] lines)
  {
    // Initialize
    this._nums = new string[5][];
    for (int i = 0; i < 5; i++) {
      this._nums[i] = new string[5];
    }
    this._numMap = new Dictionary<string, Point>();
    // Parse
    int cnt = 0;
    foreach (string row in lines) {
      string[] nums = row.Trim().Replace("  ", " ").Split(" ");
      foreach (string num in nums) {
        int r = cnt / 5;
        int c = cnt % 5;
        this._nums[r][c] = num;
        this._numMap.Add(num, new Point(r, c));
        cnt++;
      }
    }
  }

  public bool CheckBingo(int row, int col) {
    bool rowBingo = true;
    bool colBingo = true;
    // Eval each row
    for (int i = 0; i < 5; i++) {
      rowBingo = rowBingo && (this._nums[i][col] == "");
      colBingo = colBingo && (this._nums[row][i] == "");
      if (!rowBingo && !colBingo) return false;
    }
    return rowBingo || colBingo;
  }

  public bool MarkNumber(string number) {
    // First, check for the number's existence on the board
    if (this._numMap.ContainsKey(number)) {
      // Second, remove the number by clearing the string
      Point p = this._numMap[number];
      this._nums[p.r][p.c] = ""; // Clear it!
      // Third, check for BINGO
      return CheckBingo(p.r, p.c);
    }
    return false;
  }

  public int BoardSum() {
    int sum = 0;
    for (int r = 0; r < 5; r++) {
      for (int c = 0; c < 5; c++) {
        string cur = this._nums[r][c];
        if (cur != "") {
          sum += int.Parse(cur);
        }
      }
    }
    return sum;
  }

  // For debugging!
  public override string ToString() {
    string line = "\t";
    for (int r = 0; r < 5; r++) {
      for (int c = 0; c < 5; c++) {
        line += this._nums[r][c] + "\t";
      }
      line += "\n\t";
    }
    return line;
  }
}

// Main method/class wrapper
public class Solution
{
  public static void Part1(string[] draws, List<Board> boards)
  {
    Stopwatch s = new Stopwatch();
    s.Start();
    int part1 = 0;
    foreach (string draw in draws) {
      bool bingo = false;
      foreach (Board b in boards) {
        bingo = b.MarkNumber(draw);
        if (bingo) {
          part1 = int.Parse(draw) * b.BoardSum();
          break;
        }
      }
      if (bingo) break;
    }
    s.Stop();
    
    System.Console.WriteLine("Part 1: " + part1 + " (" + s.Elapsed.Milliseconds + "ms)");
  }

  public static void Main(string[] args)
  {
    string fileName = "input.txt";
    if (args.Length == 1 && args[0] == "-sample") {
      fileName = "sample_input.txt";
    }

    string[] lines = System.IO.File.ReadAllLines(fileName);
    // First line will always be the numbers drawn for Bingo.
    // Every subsequent group of 5 lines is a Bingo board.
    string[] draws = lines[0].Split(",");

    List<Board> boards = new List<Board>();
    for (int ln = 2; ln < lines.Length; ln += 6) {
      string[] boardLines = new string[5];
      for (int i = 0; i < 5; i++)
      {
        boardLines[i] = lines[ln + i];
      }
      boards.Add(new Board(boardLines));

      // Debug prints
      //Console.WriteLine(boards[boards.Count - 1]);
      //Console.WriteLine();
    }
    
    // Boards are set up, now we cross off each number!
    Part1(draws, boards);
  }
}
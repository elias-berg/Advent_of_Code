// Advent of Code 2022 - Day 20
// Grove Positioning System
//
// Time to meet back up with the elves. Unfortunately, you can't reach them
// when you try to contact them. However, you remember that the coordinates
// that they were headed to is in an encrypted file on the communication
// device. The encrypted file is a series of numbers in a list that loops
// back to the beginning from the end. To unencrypt the file, you need to
// shift each number in the order they originally appear in the list by
// the number of positions denoted by the number itself. E.g. 1 will shift
// one position right, -2 will shift two positions left, etc.
//
// Part 1 -
// Given the input of numbers, unencrypt the file as described by the rules
// and then find the 1000th, 2000th, and 3000th number after the 0.
// What is the sum of these three numbers?

// To run:
// - Make sure you have a JDK installed.
// - In a terminal, run the command: java solution.java
// - Voila

import java.io.File;
import java.util.Scanner;
import java.util.ArrayList;

public class solution {
  /**
   * Linked List individual node.
   */
  public class Node {
    public Node Prev;
    public Node Next;
    public int Value;
    public Node(int v) {
      this.Value = v;
    }
    /**
     * Set the references and return the next node!
     * @param v Next node value.
     * @return The "Next" node.
     */
    public Node SetNext(int v) {
      Node next = new Node(v);
      this.Next = next;
      next.Prev = this;
      return next;
    }
    /**
     * Shifts the node over one position to the left.
     */
    public void ShiftLeft() {
      Node prev = this.Prev;
      Node next = this.Next;
      prev.Next = next;
      next.Prev = prev;
      // Now shift over
      Node prevPrev = prev.Prev;
      prevPrev.Next = this;
      this.Prev = prevPrev;
      this.Next = prev;
      prev.Prev = this;
    }
    /**
     * Shifts the node over one position to the right.
     */
    public void ShiftRight() {
      Node prev = this.Prev;
      Node next = this.Next;
      prev.Next = next;
      next.Prev = prev;
      // Now shift over
      Node nextNext = next.Next;
      nextNext.Prev = this;
      this.Next = nextNext;
      this.Prev = next;
      next.Next = this;
    }
  }

  // The values of the encrypted file in the order that they originally appear.
  public ArrayList<Node> OrderedValues;

  // O(1) access to the "start" Node for the decryption reading.
  public Node Zero;

  /**
   * Parses the input file into a Linked List and order-preserved array.
   * @param fileName Name of the file to parse.
   */
  public void ParseInput(String fileName) {
    this.OrderedValues = new ArrayList<Node>();

    File f = new File(fileName);
    Scanner s = null;
    try {
        s = new Scanner(f);

        int val = s.nextInt();
        Node first = new Node(val);
        this.OrderedValues.add(first);
        if (val == 0) {
          this.Zero = first;
        }

        Node current = first;
        while (s.hasNextInt()) {
          val = s.nextInt();
          current = current.SetNext(val);
          if (val == 0) {
            this.Zero = current;
          }
          this.OrderedValues.add(current);
        }

        first.Prev = current;
        current.Next = first;

    } catch (Exception e) {
      System.err.println("Error reading input file.");
      System.exit(1);
    } finally {
      // Don't forget to close the file reader
      if (s != null) s.close();
    }
  }

  /**
   * Shift each node in the order they appeared within the Linked List.
   */
  public void Decrypt() {
    //int size = this.OrderedValues.size();
    for (Node n : this.OrderedValues) {
      int val = n.Value;

      if (val != 0) {
        if (val < 0) { // Shift left
          while (val < 0) {
            n.ShiftLeft();
            val++;
          }
        } else if (val > 0) { // Shift right
          while (val > 0) {
            n.ShiftRight();
            val--;
          }
        }
      }
    }
  }

  /**
   * Output the solution for Part 1:
   * Sum of the values at the 1,000th, 2,000th, and 3,000th positions.
   */
  public void Part1() {
    int sum = 0;
    int count = 0;
    Node current = this.Zero;
    // Yeah it's a bit brutish, but we might as well for ease of coding
    while (count <= 3000) {
      count++;
      current = current.Next;

      if (count == 1000 || count == 2000 || count == 3000) {
        //System.err.println("Found " + current.Value);
        sum += current.Value;
      }
    }

    System.err.println("Part 1: " + sum);
  }

  /**
   * For debugging.
   * @param s Current state of the solution to print.
   */
  public static void PrintList(solution s) {
    Node n = s.Zero;
    do {
      System.out.print(n.Value);
      n = n.Next;
      if (n.Value != 0) {
        System.out.println();
      }
    } while (n.Value != 0);
  }
  public static void main(String[] args) {
    String fileName = "input.txt";
    if (args.length == 1 && args[0].equals("-sample")) {
      fileName = "sample_input.txt";
    }

    solution day20 = new solution();
    day20.ParseInput(fileName);
    day20.Decrypt();
    day20.Part1();
  }
}
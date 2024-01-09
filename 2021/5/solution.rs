use std::io::prelude::*;
use std::fs::File;
use std::collections::HashMap;
use std::env;
use std::cmp::*;
use std::time::SystemTime;

#[derive(Debug)]
#[derive(Eq, Hash, PartialEq)]
struct Point {
  x: i32,
  y: i32,
}

#[derive(Debug)]
struct Line {
  a: Point,
  b: Point,
}

/**
 * Convert a string point in the format x,y into
 * a Point struct.
 */
fn parse_tuple(point: &str) -> Point {
  let c_idx = point.find(',').unwrap();
  let x = point.get(0..c_idx).unwrap();
  let y = point.get(c_idx + 1..).unwrap();
  
  { Point 
    { x: x.parse().unwrap(),
      y: y.parse().unwrap()
    }
  }
}

/**
 * Convert a line of text into a Line, which is a start
 * point and an end point.
 */
fn parse_line(line: Option<&str>) -> Line {
  if let Some(cur) = line {
    let idx1 = cur.find(' ').unwrap();
    let idx2 = cur.rfind(' ').unwrap();
    let (a, _) = cur.split_at(idx1);
    let (_, b) = cur.split_at(idx2 + 1);
    (return Line {
      a: parse_tuple(a),
      b: parse_tuple(b)
    });
  }

  Line { a: { Point { x: 0, y: 0 } }, b: { Point { x: 0, y: 0 } } }
}

/**
 * Part 1: only process straight lines. I.e. where p1.x == p2.x or
 * p1.y == p2.y. Count the points that end up one two or more lines.
 */
fn part1(rays: &Vec<Line>, map: &mut HashMap<String, i32>) -> i32 {
  let mut count = 0;

  for ray in rays {
    let p1 = &ray.a;
    let p2 = &ray.b;
    // TODO: Modularize this if-else block since it can be genericized
    if p1.x == p2.x { // Y-axis ray
      let same = p1.x;
      let max = max(p1.y, p2.y);
      let min = min(p1.y, p2.y);
      let dist = max - min;
      for i in 0..dist + 1 {
        let p: String = format!("{},{}", same.to_string(), (min + i).to_string());
        let entry = *map.entry(p).and_modify(|val| *val += 1).or_insert(1);
        if entry == 2 {
          count += 1
        }
      }
    } else if p1.y == p2.y { // X-axis ray
      let same = p1.y;
      let max = max(p1.x, p2.x);
      let min = min(p1.x, p2.x);
      let dist = max - min;
      for i in 0..dist + 1 {
        let p: String = format!("{},{}", (min + i).to_string(), same.to_string());
        let entry = *map.entry(p).and_modify(|val| *val += 1).or_insert(1);
        if entry == 2 {
          count += 1
        }
      }
    }
  }

  count
}

/**
 * For Part 2, we'll already have part 1 done, so we'll go back through the
 * list of lines and now accumulate the ones that are diagonals.
 */
fn part2(rays: &Vec<Line>, map: &mut HashMap<String, i32>) -> i32 {
  let mut count = 0;

  for ray in rays {
    let p1 = &ray.a;
    let p2 = &ray.b;
    if p1.x != p2.x && p1.y != p2.y {
      let mut x_dir = 1; // Assume x increases from p1 to p2
      let mut y_dir = 1; // Assume y increases from p1 to p2
      if p1.x > p2.x {
        x_dir = -1;
      }
      if p1.y > p2.y {
        y_dir = -1;
      }
      let dist = (p1.x - p2.x).abs();

      // Now move across each point
      let x = p1.x;
      let y = p1.y;
      for i in 0..dist + 1 {
        let p: String = format!("{},{}", (x + (i * x_dir)).to_string(), (y + (i * y_dir)).to_string());
        map.entry(p).and_modify(|val| *val += 1).or_insert(1);
      }
    }
  }

  // We already used up the trick to count as we go in Part 1. If we wanted to do that here,
  // then we'd combine the Part 1 code and throw in the conditional in the loop above in with
  // it and continue to count as we go. So to accomodate having code for both parts in this
  // one code file, we'll just go through and count all the collisions individually.
  for key in map.keys() {
    match map.get(key) {
      Some(&val) => {
        if val >= 2 {
          count += 1;
        }
      }
      None => {
        continue;
      }
    }
  }

  count
}

fn main() -> std::io::Result<()> {
  // Parse command line args to check for sample input flag
  let mut input_file = "input.txt";

  let args: Vec<String> = env::args().collect();
  if args.len() >= 2 && args[1] == "-sample" {
    input_file = "sample_input.txt";
  }

  // Read in the input file
  let mut file = File::open(input_file)?;
  let mut contents = String::new();
  file.read_to_string(&mut contents)?;

  // Start the Part 1 timer to include parsing the input
  let mut start = SystemTime::now();

  // Find the max number in all of the coordinates since that will determine the size of the grid
  let mut lines = contents.lines();
  // For each line, we need to split on " -> "
  // Then for each point, we need to split on "," and parse each half
  let mut rays: Vec<Line> = Vec::new();
  let mut line = lines.next();
  while line != None {
    rays.push(parse_line(line));
    line = lines.next();
  }

  // Part 1
  // Find all of the points that exist across two or more straight lines
  let mut all_points: HashMap<String, i32> = HashMap::new();
  let count = part1(&rays, &mut all_points);
  let mut elapsed = SystemTime::now().duration_since(start).expect("?");
  println!("Part 1: {count} ({elapsed:?})");
  
  // Part 2
  // Find all of the points that exist across two or more straight or diagonal lines
  start = SystemTime::now();
  let count = part2(&rays, &mut all_points);
  elapsed = SystemTime::now().duration_since(start).expect("?");
  println!("Part 2: {count} ({elapsed:?})");

  Ok(())
}
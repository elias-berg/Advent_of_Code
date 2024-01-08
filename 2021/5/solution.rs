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
struct Ray {
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
 * Convert a line of text into a Ray, which is a start
 * point and an end point.
 */
fn parse_line(line: Option<&str>) -> Ray {
  if let Some(cur) = line {
    let idx1 = cur.find(' ').unwrap();
    let idx2 = cur.rfind(' ').unwrap();
    let (a, _) = cur.split_at(idx1);
    let (_, b) = cur.split_at(idx2 + 1);
    (return Ray {
      a: parse_tuple(a),
      b: parse_tuple(b)
    });
  }

  Ray { a: { Point { x: 0, y: 0 } }, b: { Point { x: 0, y: 0 } } }
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
  let start = SystemTime::now();

  // Find the max number in all of the coordinates since that will determine the size of the grid
  let mut lines = contents.lines();
  // For each line, we need to split on " -> "
  // Then for each point, we need to split on "," and parse each half
  let mut rays: Vec<Ray> = Vec::new();
  let mut line = lines.next();
  while line != None {
    rays.push(parse_line(line));
    line = lines.next();
  }

  // Part 1
  // Find all of the rays that appear for multiple straight lines
  let mut all_points: HashMap<String, i32> = HashMap::new();
  for ray in rays {
    let p1 = ray.a;
    let p2 = ray.b;
    // TODO: Modularize this if-else block since it can be genericized
    if p1.x == p2.x { // Y-axis ray
      let same = p1.x;
      let max = max(p1.y, p2.y);
      let min = min(p1.y, p2.y);
      let dist = max - min;
      for i in 0..dist + 1 {
        let p: String = same.to_string() + "," + &(min + i).to_string();
        all_points.entry(p).and_modify(|val| *val += 1).or_insert(1);
      }
    } else if p1.y == p2.y { // X-axis ray
      let same = p1.y;
      let max = max(p1.x, p2.x);
      let min = min(p1.x, p2.x);
      let dist = max - min;
      for i in 0..dist + 1 {
        let p: String = (min + i).to_string() + "," + &same.to_string();
        all_points.entry(p).and_modify(|val| *val += 1).or_insert(1);
      }
    }
  }

  // Now count all of the point collisions by going through each key
  let mut count = 0;
  for key in all_points.keys() {
    match all_points.get(key) {
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
  let elapsed = SystemTime::now().duration_since(start)
      .expect("?");
  println!("Part 1: {count} ({elapsed:?})");
  
  Ok(())
}
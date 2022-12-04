use std::collections::BinaryHeap;
use std::fs::read_to_string;
use std::path::Path;

pub fn run(input_dir: &Path) {
    let input_path = input_dir.join("day01");
    let input_data = read_to_string(input_path).expect("Day 01 input data could not be read!");
    let mut heap = BinaryHeap::new();
    let mut total = 0;
    for line in input_data.lines() {
        match line.parse::<i32>() {
            Ok(calories) => total += calories,
            Err(_error) => {
                heap.push(total);
                if heap.len() > 3 {
                    heap.pop();
                }
                total = 0;
            }
        }
    }
    let mut total = 0;
    total += heap.pop().unwrap();
    total += heap.pop().unwrap();
    let max = heap.pop().unwrap();
    total += max;
    println!("{max}");
    println!("{total}");
}

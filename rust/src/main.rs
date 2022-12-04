use std::env;
use std::path::Path;
mod days;
fn main() {
    let args: Vec<String> = env::args().collect();
    let filedir = Path::new(&args[1]);

    days::day01::run(filedir);
}

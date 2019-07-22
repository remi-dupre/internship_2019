extern crate regex;

use regex::Regex;

use std::env;
use std::fs;
use std::io::prelude::*;
use std::io::{stdin, stdout};

fn main() {
    let mut argv = env::args();
    argv.next(); // program name

    let regex = argv.next().expect("Usage: naive <regexp> [filename]");
    let filename = argv.next();

    // Read the text
    let mut text = String::new();
    match filename {
        None => {
            stdin().read_to_string(&mut text).unwrap();
        }
        Some(filename) => {
            let mut file = fs::File::open(filename).unwrap();
            file.read_to_string(&mut text).unwrap();
        }
    }

    // Remove trailing newlines
    while text.as_bytes().last() == Some(&b'\n') {
        text.pop();
    }
    text = text.trim_end_matches(r"\n").to_string();

    // Match all possible substrings
    let regex = Regex::new(&format!("^{}$", regex)).unwrap();

    for i in 0..text.len() {
        for j in i..text.len() {
            if regex.is_match(&text[i..j]) {
                println!("{},{}", i, j);
            }
        }
    }

    println!("Hello, world!");
}

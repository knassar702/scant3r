use std::fs::File;
use std::io::{BufRead, BufReader};
use std::path::Path;
use home::home_dir;


pub asnyc fn scan() {
    let path = Path::new(home_dir()).join(".subtakeover");
    let file = File::open(path).unwrap();
    let reader = BufReader::new(file);
    for line in reader.lines() {
        let line = line.unwrap();
        let mut parts = line.split(" ");
        let host = parts.next().unwrap();
        let port = parts.next().unwrap();
        let username = parts.next().unwrap();
        let password = parts.next().unwrap();
        println!("{} {} {} {}", host, port, username, password);
    }

}

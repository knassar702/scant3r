use home::home_dir;
use std::path::Path;
use std::fs::create_dir;

const MODULES: [&str; 1] = ["xss"];

pub fn check_config() {
        let init_dir = home_dir().unwrap().join(".scant3r");
        match Path::new(&init_dir).exists() {
            true => {},
            false => {
                match create_dir(&init_dir) {
                    Ok(_dir) => {},
                    Err(e) => {
                        println!(" ERROR: Failed to Create config folder : {}",e);
                        println!(" ERROR: EXIT");
                        std::process::exit(0);
                    }
                }
            }
        };

        MODULES.iter().for_each(|module| {
            match Path::new(module).exists() {
                true => {},
                false => {
                    println!(" ERROR: Module folder not found, create another one");
                    match create_dir(module) {
                        Ok(_dir) => {},
                        Err(e) => {
                            println!(" ERROR: Failed to Create module folder : {}",e);
                            std::process::exit(0);
                        }
                    }
                }
            };
        });
    }


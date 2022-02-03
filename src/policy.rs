use serde::{Serialize, Deserialize};

#[derive(Debug, PartialEq, Serialize, Deserialize)]
pub struct Policy {
    pub name: String,
    pub description: String,
    pub config: String
}


pub fn get_policy(name: &str) -> String {
    let mut policy = Policy {
        name: String::from(name),
        description: String::from(""),
        config: String::from("")
    };
    let json = serde_json::to_string(&policy).unwrap();
}

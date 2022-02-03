

pub struct Policy {
    pub name: String,
    pub description: String,
    pub config: String
}

impl Policy {
    pub fn new(name: String, description: String, config: String) -> Policy {
        Policy {
            name: name,
            description: description,
            config: config
        }
    }

}

pub struct Poc {
    pub name: String,
    pub bruh: String,
}


pub trait Curl {
    fn curl(&self) -> String;
}

impl Curl for Poc {
    fn curl(&self) -> String {
        format!("curl -X POST -H 'Content-Type: application/json' -d '{}' {}", self.name, self.bruh)
    }
}


pub trait Plain {
    fn plain(&self) -> String;
}

impl Plain for Poc {
    fn plain(&self) -> String {
        format!("{} {}", self.name, self.bruh)
    }
}


pub trait Json {
    fn json(&self) -> String;
}

impl Json for Poc {
    fn json(&self) -> String {
        format!("{} {}", self.name, self.bruh)
    }
}

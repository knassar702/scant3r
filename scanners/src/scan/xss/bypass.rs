
pub struct Analyzer {
    pub response: String,
    pub payload: String,
}

impl Analyzer {
    pub fn new(response: String, payload: String) -> Analyzer {
        Analyzer {
            response: String::new(),
            payload: String::new(),
        }
    }

    pub fn analize(&self) -> String {
        String::new()
    }

    pub fn gen_payload(&self) -> String {
        String::new()
    }
}


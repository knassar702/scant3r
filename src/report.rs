#[ path = "report.rs"]
mod requests;
use crate::requests::Msg;

struct Report {
    folder: String,
    request: Msg,
}


impl Report {
    fn new(request: Msg,folder: String) -> Report {
        Report {
            folder,
            Msg
        }
    }

    fn generate(&self) {
        println!("Generating report for {}", self.folder);
    }
}

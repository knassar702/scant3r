#[path = "../requests.rs"]
mod requests;
#[path = "../payloads.rs"]
mod payloads;
use crate::requests::Msg;

const PAYLOAD: &str = include_str!("../txt/xss.txt");

pub fn scan(mut request: Msg ) {
    let mut url = request.url.clone();
    let mut test = payloads::Injector::new(url);
    for payload in PAYLOAD.split("\n"){
        let scan = test.url_parameters(payload);
        for url in scan.iter() {
            request.url = url.clone();
            request.send();
            if &payload.len() > &0 {
                if request.response_body.as_ref().unwrap().contains(&payload) {
                    println!("[+] {}", &payload);
                    println!("[+] XSS found in {}", url);
                }
            }
        }
    }
}

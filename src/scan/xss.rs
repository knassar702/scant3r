#[path = "../requests.rs"]
mod requests;
#[path = "../payloads.rs"]
mod payloads;
use crate::requests::Msg;
#[path = "mod.rs"] 
mod scan;

pub async fn scan(mut request: Msg ,payloads: &Vec<String>) -> bool {
    let inject_payloads = payloads::Injector{
        request: request.url
    };
    for payload in payloads {
        let scan = inject_payloads.url_parameters(payload.as_str());
        for (param,urls) in scan.iter() { 
            for url in urls {
                request.url = url.clone();
                request.send();
                if payload.len() > 0 && request.response_body.as_ref().unwrap().contains(payload.as_str()) {
                        println!("[+] {}", url);
                        return true;
                    }
                }
        }
    }
    false
}

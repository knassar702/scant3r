#[path = "../requests.rs"]
mod requests;
#[path = "../payloads.rs"]
mod payloads;
use futures::lock::Mutex;
use crate::requests::Msg;

pub async fn scan(mut request: Msg ) {
    let mutex = Mutex::new(0);
    let mut _payload;
    let test = payloads::Injector{
        request: request.url
    };
    {
        mutex.lock();
        _payload = std::fs::read_to_string("/home/knassar702/.scant3r/ssrf.txt").unwrap();
    }
    for payload in _payload.split("\n"){
        let scan = test.url_parameters(payload);
        for (param,urls) in scan.iter() { 
            for url in urls {
                request.url = url.clone();
                request.send();
                if payload.len() > 0 && request.response_body.as_ref().unwrap().contains(&payload) {
//                        println!("[+] {} {}", request.url, &payload);
                        break;
                    }
                }
        }
    }
}

#[path = "../requests.rs"]
mod requests;
#[path = "../payloads.rs"]
mod payloads;
use crate::requests::Msg;
use std::collections::HashMap;


pub async fn scan(request: Msg ,payloads: &Vec<String>) -> bool {
    let inject_payloads = payloads::Injector{
        request: request.clone().url
    };
    let mut reflected = HashMap::new();
    // check for reflected parameters
    for payload in payloads {
        let _reflect = inject_payloads.url_parameters("scantrr");
        for (_param,urls) in _reflect {
            for url in urls {
                let _param = _param.clone();
                let mut req = request.clone();
                req.url = url.clone();
                req.send().await;
                if req.response_body.unwrap().contains("scantrr") {
                    reflected.insert(_param,url.clone());
                }
            }
        }
        // change a custom parameter value
        for (param,url) in reflected.clone() {
            let mut req = request.clone();
            req.url = url.clone();
            let new_params = {
                    let params = req.url.query_pairs().into_iter().collect::<HashMap<_, _>>();
                    let mut params2 = HashMap::new();
                    for (key,value) in params.clone() {
                        params2.insert(key.to_string(),value.clone().to_string());
                    }
                    *params2.get_mut(&param).unwrap() = payload.to_string();
                    params2
            };
            req.url = {
                req.url.query_pairs_mut().clear();
                for (key,value) in new_params {
                    req.url.query_pairs_mut().append_pair(&key,&value);
                }
                req.url
            };
            req.send().await;
            if req.response_body.unwrap().contains(payload) {
                println!("[+] XSS found in {} on {}",req.url,param);
            }
            break;
        }
    }
    false
}

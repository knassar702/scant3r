#[path = "../requests.rs"]
mod requests;
#[path = "../payloads.rs"]
mod payloads;
#[ path = "../report.rs" ]
mod report;
use payloads::url_injector;
use crate::requests::Msg;
use std::collections::HashMap;

pub struct Xss {
    request: Msg,
    inject_body: bool,
    inject_query: bool,
    injector: payloads::Injector,
}

impl Xss {
    pub fn new(request: Msg,inject_body: bool, inject_query: bool) -> Xss {
        Xss {
            request: request.clone(),
            inject_body,
            inject_query,
            injector: payloads::Injector{request: request.url},
        }
    }

    pub async fn find_reflected(&self) -> HashMap<String,url::Url> {
        let mut reflected_parameters: HashMap<String,url::Url> = HashMap::new();
        let check_requests = self.injector.url_parameters("scantrr");
        for (_param,urls) in check_requests {
            for url in urls {
                let _param = _param.clone();
                let mut req = self.request.clone();
                req.url = url.clone();
                req.send().await;
                if req.response_body.unwrap().contains("scantrr") {
                    reflected_parameters.insert(_param,url.clone());
                }
            }
        }
        reflected_parameters
    }

    pub async fn scan(&self,payloads: &Vec<String>) -> bool {
        for (param,url) in self.find_reflected().await {
            for payload in payloads {
                let mut req = self.request.clone();
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
                let body = req.response_body.unwrap();
                if body.contains(payload) {
                    body.lines().enumerate().for_each(|x|{
                        if x.1.contains(payload) == true {
                            println!("XSS");
                        }
                    });
                    break;
                } else {
                    continue;
                }
            }
        }
        false
    }
}

extern crate scant3r_utils;

use scant3r_utils::{
    Injector::{
        Urlinjector,
        Injector
    },
    poc::{
        Poc,
        Curl
    },
    requests::Msg
};
use async_trait::async_trait;
use std::collections::HashMap;
use indicatif::ProgressBar;
use console::Emoji;

// create a struct with refrence Vec


pub struct Xss<'t> {
    request: &'t Msg,
    injector: Injector,
}


#[async_trait]
pub trait XssUrlParamsName {
    async fn name_reflected(&self) -> ();
    async fn name_scan(&self, payloads: Vec<String>,_prog: &ProgressBar) -> ();
}

#[async_trait]
pub trait XssUrlParamsValue {
    // scan url params value
    async fn value_reflected(&self) -> HashMap<String,url::Url>;
    async fn value_scan(&self, payloads: Vec<String>,_prog: &ProgressBar) ->HashMap<url::Url, String>;
}



impl Xss<'_> {
    pub fn new(request: &Msg) -> Xss<'_> {
        Xss {
            request,
            injector: Injector{request: request.url.clone()},
        }
    }

}



#[async_trait]
impl XssUrlParamsName for Xss<'_> {
    async fn name_reflected(&self) -> () {
    }

    async fn name_scan(&self,_payloads: Vec<String>, _prog: &ProgressBar) -> () {

    }
}

#[async_trait]
impl XssUrlParamsValue for Xss<'_> {

    async fn value_reflected(&self) -> HashMap<String,url::Url>  {
        let mut reflected_parameters: HashMap<String,url::Url> = HashMap::new();
        let check_requests = self.injector.url_value("scanttrr");
        for (_param,urls) in check_requests {
            for url in urls {
                let _param = _param.clone();
                let mut req = self.request.clone();
                req.url = url.clone();
                let resp = &req.send().await.unwrap();
                if resp.body.contains("scanttrr") {
                    reflected_parameters.insert(_param,url.clone());
                }
            }
        }
        reflected_parameters
    }

    async fn value_scan(&self,payloads: Vec<String>,_prog: &ProgressBar) -> HashMap<url::Url, String>{
        let mut _found: HashMap<url::Url,String> = HashMap::new();
        for (param,url) in self.value_reflected().await {

            for payload in &payloads {

                let mut req = self.request.clone();
                req.url = self.injector.set_urlvalue(&param, payload, url.clone());
                let res = req.send().await.unwrap_or_else(|_| panic!("asfkasofk"));
                if res.body.contains(payload) {
                    res.body.lines()
                        .enumerate()
                        .for_each(|(line,found)|{

                            if found.contains(payload) == true {
                                let report = Poc {
                                    name: "sg".to_owned(),
                                    payload: payload.to_owned(),
                                    request: &req,
                                };
                                // alert emoji
                                let m = format!("{} {}\nLine: {}",Emoji("🚨", "alert"),report.curl(),&line);
                                _prog.println(&m);
                                _found.insert(req.url.clone(),m);
                            }
                    });
                    break;
                } else {
                    continue;
                }
            }
        }
        _found
    }
}

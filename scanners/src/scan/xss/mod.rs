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
use crate::url_encode;

mod parser;
use parser::{
    parse,
    html_search,
    Location
};
mod bypass;
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
        let mut bruh: HashMap<String,(url::Url,Vec<Location>)> = HashMap::new();
        let check_chars = vec!["<",">","'","\"","=","`","/"," "];
        let mut check_allowed: Vec<&str> = Vec::new();
        let check_requests = self.injector.url_value("scanttrr");
        for (_param,urls) in check_requests {
            for url in urls {
                let _param = _param.clone();
                let mut req = self.request.clone();
                req.url = url.clone();
                let resp = &req.send().await.unwrap();
                let t = parse(resp.body.as_str(), "scanttrr".to_string());
                if t.len() > 0 {
                    bruh.insert(_param.clone(),(url.clone(),t));
                }
                if resp.body.contains("scanttrr") {
                    for Char in check_chars.iter() {
                        let c = self.injector.set_urlvalue(_param.as_str(), format!("scant3rrr{}",Char).as_str());
                        let mut req = self.request.clone();
                        req.url = c.clone();
                        let resp = &req.send().await.unwrap();
                        let t = parse(resp.body.as_str(), Char.to_string());
                        if t.len() > 0 {
                            bruh.insert(_param.clone(),(url.clone(),t));
                        }
                    }
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

                if payload.len() == 0 {
                    continue;
                }
                let mut req = self.request.clone();
                req.url = self.injector.set_urlvalue(&param, payload);
                let res = req.send().await.unwrap_or_else(|_| panic!("asfkasofk"));
                let _find = parse(res.body.as_str(), payload.to_string().replace("\n", ""));
                if _find.len() > 0 {
                    _find.iter().for_each(|x| {
                        match x {
                            Location::AttrName(name) => {
                                println!("ATTR NAME {:?}", name);
                            },
                            Location::AttrValue(value) => {
                                println!("ATTR VALUE {:?}", value);
                            },
                            Location::TagName(name) => {
                                println!("TAG NAME {:?}", name);
                            },
                            Location::Comment(comment) => {
                                req.url = self.injector.set_urlvalue(&param, "--><img src=x onerror=alert()>");
                            },
                            Location::Text(text) => {
                                println!("TEXT {:?}", text);
                            },
                            e => {
                                println!("{:?}", e);
                            }
                        }
                    });
                    let resp = html_search(req.send().await.unwrap_or_else(|_| panic!("asfkasofk")).body.as_str(), "a[onclick=alert()]");
                    println!("{:?}", resp);

                } else {
                    continue;
                }
            }
        }
        _found
    }
}

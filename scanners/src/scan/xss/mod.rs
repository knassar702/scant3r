extern crate scant3r_utils;

use crate::model::Report;
use console::style;
use indicatif::ProgressBar;
use log::error;
use scant3r_utils::{
    injector::{Injector, Urlinjector},
    random_str,
    requests::{Curl, Msg},
};

mod parser;
use parser::{html_parse, html_search};

mod bypass;
pub use bypass::{PayloadGen, XssPayloads};

pub fn print_poc(report: &Report) -> String {
    format!(
        "\n{}\n{} URL: {}\n{} MATCH: {}\n{} PAYLOAD: \"{}\"\n{} CURL: {}\n",
        style("[XSS]").bold().red(),
        style(">> ").yellow(),
        report.url,
        style(">> ").yellow(),
        report.match_payload,
        style(">> ").yellow(),
        report.payload.replace("\"", "\\\""),
        style(">> ").yellow(),
        report.curl,
    )
}

fn get_cspcheck() -> Vec<&'static str> {
    vec![
        ".doubleclick.net",
        ".googleadservices.com",
        "cse.google.com",
        "accounts.google.com",
        "*.google.com",
        "www.blogger.com",
        "*.blogger.com",
        "translate.yandex.net",
        "api-metrika.yandex.ru",
        "api.vk.comm",
        "*.vk.com",
        "*.yandex.ru",
        "*.yandex.net",
        "app-sjint.marketo.com",
        "app-e.marketo.com",
        "*.marketo.com",
        "detector.alicdn.com",
        "suggest.taobao.com",
        "ount.tbcdn.cn",
        "bebezoo.1688.com",
        "wb.amap.com",
        "a.sm.cn",
        "api.m.sm.cn",
        "*.taobao.com",
        "*.tbcdn.cn",
        "*.1688.com",
        "*.amap.com",
        "*.sm.cn",
        "mkto.uber.com",
        "*.uber.com",
        "ads.yap.yahoo.com",
        "mempf.yahoo.co.jp",
        "suggest-shop.yahooapis.jp",
        "www.aol.com",
        "df-webservices.comet.aol.com",
        "api.cmi.aol.com",
        "ui.comet.aol.com",
        "portal.pf.aol.com",
        "*.yahoo.com",
        "*.yahoo.jp",
        "*.yahooapis.jp",
        "*.aol.com",
        "search.twitter.com",
        "*.twitter.com",
        "twitter.com",
        "ajax.googleapis.com",
        "*.googleapis.com"
    ]
}

pub fn valid_to_xss(req: &Msg) -> (bool,bool) {
        let block_headers = vec![
            "application/json",
            "application/javascript",
            "text/javascript",
            "text/plain",
            "text/css",
            "image/jpeg",
            "image/png",
            "image/bmp",
            "image/gif",
            "application/rss+xml",
        ];

        let mut is_html = false;
        let mut need_manual_check = false;
        match req.send() {
            Ok(resp) => { 
                for csp in get_cspcheck().iter() {
                    if resp.headers.get("Content-Security-Policy").is_some() {
                        if resp.headers.get("Content-Security-Policy").unwrap().to_str().unwrap().contains(csp) {
                            need_manual_check = true;
                        }
                    }
                }
                block_headers.iter().for_each(|header| {
                if resp.headers.contains_key("Content-Type") {
                    if resp.headers.get("Content-Type").unwrap() == header {
                        is_html = true;
                    }
                } else {
                    is_html = true;
                }
            })

            },
            Err(e) => {
                error!("{}", e);
                return (false,false);
            }
        }
        (is_html,need_manual_check)
    }


pub struct Xss<'t> {
    request: &'t Msg,
    injector: Injector,
    payloads: &'t XssPayloads,
}

pub trait XssUrlParamsValue {
    fn value_reflected(&self) -> Vec<String>;
    fn value_scan(&self, _prog: &ProgressBar) -> Vec<Report>;
}

impl Xss<'_> {
    pub fn new<'a>(request: &'a Msg, payloads: &'a XssPayloads, keep_value: bool) -> Xss<'a> {
        Xss {
            request,
            payloads,
            injector: Injector {
                request: request.url.clone(),
                keep_value,
            },
        }
    }
}

impl XssUrlParamsValue for Xss<'_> {

    fn value_reflected(&self) -> Vec<String> {
        let mut reflected_parameters: Vec<String> = Vec::new();
        let payload = random_str(5);
        let check_requests = self.injector.url_value(&payload);
        for (_param, urls) in check_requests {
            for url in urls {
                let _param = _param.clone();
                let mut req = self.request.clone();
                req.url = url.clone();
                match req.send() {
                    Ok(resp) => {
                        let found = resp.body.contains(&payload);
                        if found {
                            reflected_parameters.push(_param);
                        }
                    }
                    Err(e) => {
                        error!("{}", e);
                        continue;
                    }
                };
            }
        }
        reflected_parameters
    }

    fn value_scan(&self, _prog: &ProgressBar) -> Vec<Report> {
        let mut _found: Vec<Report> = Vec::new();
        for param in self.value_reflected() {
            let mut req = self.request.clone();
            let payload = random_str(5).to_lowercase();
            req.url = self.injector.set_urlvalue(&param, &payload);
            let res = match req.send() {
                Ok(resp) => resp,
                Err(e) => {
                    _prog.set_message(format!("CONNECTION ERROR: {}", e));
                    continue;
                }
            };
            for reflect in html_parse(&res.body.as_str(), &payload).iter() {
                let payload_generator =
                    PayloadGen::new(&res.body.as_str(), reflect, &payload, &self.payloads);
                for pay in payload_generator.analyze().iter() {
                    let count = html_search(&res.body.as_str(), &pay.search);
                    req.url = self.injector.set_urlvalue(&param, &pay.payload);
                    match req.send() {
                        Ok(resp) => {
                            let payload_found = html_search(resp.body.as_str(), &pay.search);
                            if payload_found.len() > count.len() {
                                _found.push(Report {
                                    url: req.url.to_string(),
                                    match_payload: payload_found.clone(),
                                    payload: pay.payload.to_string(),
                                    curl: req.curl(),
                                });
                                _prog.println(print_poc(&Report {
                                    url: req.url.to_string(),
                                    match_payload: payload_found,
                                    payload: pay.payload.to_string(),
                                    curl: req.curl(),
                                }));
                                break;
                            }
                        }
                        Err(_e) => {
                            continue;
                        }
                    };
                }
            }
        }
        _found
    }
}

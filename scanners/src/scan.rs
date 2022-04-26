extern crate scant3r_utils;
use indicatif::{ProgressBar, ProgressStyle};
use rayon::iter::{IntoParallelRefIterator, ParallelIterator};
use scant3r_utils::requests::{Msg, Settings};
use console::style;

mod xss;
use xss::{valid_to_xss,XssPayloads, XssUrlParamsValue};

#[derive(Debug)]
pub enum Payloads {
    XSS(XssPayloads),
}

pub struct Scanner {
    pub modules: Vec<String>,
    pub payloads: Vec<Payloads>,
    pub requests: Vec<Msg>,
    pub keep_value: bool,
}

impl Scanner {
    pub fn new(modules: Vec<String>, requests: Vec<Msg>, keep_value: bool) -> Scanner {
        Scanner {
            modules,
            payloads: Vec::new(),
            requests,
            keep_value,
        }
    }

    pub fn load_config(&mut self) {
        self.payloads.push(Payloads::XSS(
                XssPayloads{
                    attr: vec![
                        "onmouseover".to_string(), 
                        "onmouseenter".to_string(),
                        "onmouseleave".to_string(),
                        "onmouseout".to_string(),
                        "onclick".to_string(),
                        "onmousedown".to_string(),
                        "onmouseup".to_string(),
                        "ontouchstart".to_string(),
                        "ontouchend".to_string(),
                        "ontouchmove".to_string(),
                        "onpointerenter".to_string(),
                        "onpointerleave".to_string(),
                        "onpointerover".to_string(),
                    ],
                    html_tags: vec!["<img src=x onerror=$JS_FUNC$`$JS_CMD$`>".to_string(), "<h1 $JS_FUNC$`$JS_CMD$`>".to_string(),"<h1 $JS_FUNC$($JS_CMD)".to_string()],
                    js_cmd: vec!["alert".to_string(),"confirm".to_string(),"prompt".to_string()],
                    js_value: vec!["this['ale'+'rt'](this['doc'+'ument']['dom'+'ain'])".to_string(),"document.cookie".to_string(), "document.location".to_string(),"1".to_string()],
                }
                ));
    }

    pub fn scan(&self, concurrency: usize) {
        let bar = ProgressBar::new(self.requests.len() as u64);
        bar.set_style(ProgressStyle::default_bar()
            .template("{spinner:.green} [{elapsed_precise}] [{bar:40.cyan/blue}] {pos:>7}/{len:7} {msg}")
            .tick_chars(format!("{}", "⣾⣽⣻⢿⡿⣟⣯⣷").as_str())
            .progress_chars("#>-"));
        let threader = rayon::ThreadPoolBuilder::new()
            .num_threads(concurrency)
            .build()
            .unwrap();

        threader.install(|| {
            self.requests.par_iter().for_each(|request| {
                self.modules.iter().for_each(|module| {
                    let module = module.as_str();
                    match module {
                        "xss" => {
                            let blocking_headers = valid_to_xss(request);
                            if blocking_headers.1 == true {
                                let _ = &bar.println(format!("{}: {}",style("Need Manual Test").yellow().bold(),request.url));
                            }
                            if !blocking_headers.0 && blocking_headers.1 == false {
                                for payload in self.payloads.iter() {
                                    match payload {
                                        Payloads::XSS(current_payload) => {
                                            let xss_scan = xss::Xss::new(
                                                request,
                                                current_payload,
                                                self.keep_value,
                                            );
                                            let _value = xss_scan.value_scan(&bar);
                                        }
                                    }
                                }
                            }
                        }
                        _ => {
                            panic!("Module not found");
                        }
                    }
                    bar.inc(1);
                });
            });
        });
    }
}

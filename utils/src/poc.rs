#[path = "requests.rs"] mod requests;
use crate::requests::Msg;
pub struct Poc {
    pub name: String,
    pub payload: String,
    pub request: Msg,
}


pub trait Curl {
    fn curl(&self) -> String;
}

impl Curl for Poc {
    fn curl(&self) -> String {
        // convert isahc request to curl
        let mut curl = String::from("curl ");
        // extract headers
        self.request.headers.iter()
            .for_each(|(key,value)| {
                curl.push_str(&format!("-H \"{}: {}\" ", key, value.replace("\"", "\\\"")));
        });
        // extract body
        if self.request.body.as_ref().unwrap().len() > 0 {
            curl.push_str(&format!("-d \"{:?}\" ", self.request.body.as_ref().unwrap()));
        }
        // extract url
        curl.push_str(&format!("\"{}\"", self.request.url));
        // extract method
        curl.push_str(&format!(" -X {}", self.request.method));
        // proxy
        if self.request.proxy.as_ref().unwrap().len() > 0 {
            curl.push_str(&format!(" -x {}", self.request.proxy.as_ref().unwrap()));
        }
        curl

    }
}


pub trait Plain {
    fn plain(&self) -> String;
}

impl Plain for Poc {
    fn plain(&self) -> String {
        String::from("")
    }
}


pub trait Json {
    fn json(&self) -> String;
    }

impl Json for Poc {
    fn json(&self) -> String {
        String::from("")
    }
}
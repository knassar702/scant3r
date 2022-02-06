use std::collections::HashMap;
#[ path = "../requests.rs" ]
mod requests;

pub struct Zap {
    pub request: requests::Msg
}


impl Zap {
    pub fn new(host: String, key: Option<String>) -> Self {
        let mut headers = HashMap::new();
        headers.insert("X-ZAP-API-Key".to_string(), key.unwrap_or("".to_string()));
        let request = requests::Msg::new("POST", 
                                         "http://zap",
                                         headers,
                                         None, 
                                         None,
                                         None, 
                                         Some(host));
        Self { request }
    }

    pub fn childNode(&mut self) {
        self.request.url = self.request.url.join("/JSON/core/view/childNodes/").unwrap();
        self.request.send();
        println!("{:?}", self.request.url.to_string());
        println!("{:?}", self.request.response_body.as_ref().unwrap());
    }
}

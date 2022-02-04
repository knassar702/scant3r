use std::collections::HashMap;

struct Injector {
    request: HashMap<String, String>,
    payload: String,
}


impl Injector {
    pub fn new(payload: String,request: HashMap<String,String>) -> Self {
        Injector {
            request,
            payload,
        }
    }

    pub fn headers(&self) -> Vec<HashMap<String,String>> {
        let mut headers = HashMap::new();
        let mut result = Vec::new();
        headers.insert("Content-Type".to_string(), "application/json".to_string());
        headers.insert("Accept".to_string(), "application/json".to_string());
        headers.insert("User-Agent".to_string(), "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36".to_string());
        result.push(headers);
        result
    }

    pub fn url_parameters(&self) -> HashMap<String, String> {
        let mut url_parameters = HashMap::new();
        url_parameters.insert("payload".to_string(), self.payload.clone());
        url_parameters
    }

    pub fn request_body(&self) -> String {
        self.payload.clone()
    }
}

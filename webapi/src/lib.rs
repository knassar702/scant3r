extern crate scant3r_utils;
extern crate scanners;
use scanners::scan;
use serde::Deserialize;
use scant3r_utils::requests::{Msg, Settings};
use actix_web::{get,post ,web, App, HttpServer, Responder};


#[derive(Deserialize)]
struct Scan {
    url: String,
    method: String,
}


#[post("/scan")]
async fn scan_url(scan: web::Json<Scan>) -> impl Responder {
    format!("{:?}", scan.url)
}

#[get("/hello/{name}")]
async fn greet(name: web::Path<String>) -> impl Responder {
    format!("Hello {name}!")
}

#[get("/bruh")]
async fn bruh() -> impl Responder {
    let req = Msg::new()
        .method("GET".to_string())
        .url("http://192.168.1.2:4000/search?u=ff".to_string());
    let mut v = scan::Scanner::new(vec!["xss"],vec![req]);
    v.load_payloads();
    v.scan(10).await;
    "BRUH"
}

#[actix_web::main] // or #[tokio::main]
pub async fn main(host: &str,port: u16) -> std::io::Result<()> {
    HttpServer::new(|| {
        App::new()
            .route("/hello", web::get().to(|| async { "Hello World!" }))
            .service(bruh)
            .service(greet)
            .service(scan_url)
    })
    .bind((host, port))?
    .run()
    .await
}

#[cfg(test)]
mod tests {
    #[test]
    fn it_works() {
        let result = 2 + 2;
        assert_eq!(result, 4);
    }
}

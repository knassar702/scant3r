extern crate scant3r_utils;
use scant3r_utils::requests::{Msg, Settings};
use hlua::{
    Lua,
    function1, function3, 
};
use std::fs::File;

fn bruh(name: String) -> String {
    format!("YEAH BOOYAH {}",name)
}

async fn request(url: String, method: String, body: String) -> String {
    let req = Msg::new()
            .url(url)
            .method(method)
            .body(body)
            .send().await;
    req.unwrap().body
}


pub fn execute_lua(file: &str){
    let mut lua = Lua::new();
    lua.openlibs();
    let file = File::open(file).unwrap();
    lua.set("bruh", function1(bruh));
    lua.execute_from_reader::<(),_>(file).unwrap();
    let mut c: hlua::LuaFunction<_> = lua.get("data").unwrap(); 
    let d: String = c.call_with_args("Khaled Aez ").unwrap();
    println!("{}", d);
}

extern crate scant3r_utils;
use hlua::{
    Lua,
    function1 
};
use scant3r_utils::requests::{Msg,Settings};
use std::fs::File;

fn sender(url: String) -> String {
    let req = Msg::new()
        .url(url)
        .method("GET".to_string());
    match req.send() {
        Ok(test) => println!("TEST"),
        Err(e) => println!("ERR"),
    }
    String::from("TES")
}
fn bruh(name: String) -> String {
    format!("YEAH BOOYAH {}",name)
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

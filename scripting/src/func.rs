use hlua::{
    Lua,
    LuaError,
    function1, 
};
use std::fs::File;

fn bruh(name: String) -> String {
    "YEAH BOOYAH".to_string()
}

fn request(c: String) {
    println!("request");
}

pub fn execute_lua(file: &str){
    let mut lua = Lua::new();
    let file = File::open(file).unwrap();
    lua.set("bruh", function1(bruh));
    lua.set("request", function1(request));
    lua.execute_from_reader::<(),_>(file).unwrap();
}

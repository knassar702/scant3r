extern crate scant3r_utils;
use hlua::{
    Lua,
    function1, function3, 
};
use std::fs::File;

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

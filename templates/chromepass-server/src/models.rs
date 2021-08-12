use serde::{Deserialize, Serialize};

#[derive(Deserialize, Serialize, Debug)]
pub struct Login {
    pub url: String,
    pub username: String,
    pub password: String,
}
#[derive(Deserialize, Serialize, Debug)]
pub struct Cookie {
    pub domain: String,
    pub name: String,
    pub value: String,
}

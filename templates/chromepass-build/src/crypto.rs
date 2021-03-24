use aes_gcm::aead::{generic_array::GenericArray, Aead, NewAead};
use aes_gcm::Aes256Gcm;
use winapi::um::dpapi::CryptUnprotectData;
use winapi::um::wincrypt::CRYPTOAPI_BLOB;
pub fn dpapi_decrypt(mut encrypted: Vec<u8>) -> Vec<u8> {
    let mut in_data = CRYPTOAPI_BLOB {
        cbData: encrypted.len() as u32,
        pbData: encrypted.as_mut_ptr(),
    };
    let mut out_data = CRYPTOAPI_BLOB {
        cbData: 0,
        pbData: std::ptr::null_mut(),
    };
    unsafe {
        let _ = CryptUnprotectData(
            &mut in_data,
            std::ptr::null_mut(),
            std::ptr::null_mut(),
            std::ptr::null_mut(),
            std::ptr::null_mut(),
            0,
            &mut out_data,
        );
        return Vec::from_raw_parts(
            out_data.pbData,
            out_data.cbData as usize,
            out_data.cbData as usize,
        );
    };
}
pub fn aes_decrypt(key: &Vec<u8>, data: Vec<u8>) -> Vec<u8> {
    let key = GenericArray::from_slice(&key);
    let cipher = Aes256Gcm::new(key);
    let nonce = GenericArray::from_slice(&data[3..15]);
    let plaintext = match cipher.decrypt(nonce, data[15..].as_ref()) {
        Ok(a) => a,
        Err(e) => panic!("Error: {}", e),
    };
    return plaintext;
}

import time
import json
import base64
import rsa
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

RSA_PUBLIC_KEY = "111602863222991102481735326647200948288032311528593963811533577327514848303466538610406051306025406098243393089983444437312893044780161636403121177652897602041270225936895701680484846699693780085858497152782257277015987809618250549268987149708345380138314168803776313533258899701102342689157482524625283184299"
RSA_EXPONENT = "65537"
AES_IV = "1628092121312213"

def generate_signature(params):
    import hashlib
    import base64
    
    tree_map = dict(sorted(params.items()))
    
    param_str = json.dumps(tree_map, ensure_ascii=False, separators=(',', ':'))
    
    sha512_hash = hashlib.sha512(param_str.encode('utf-8')).digest()
    
    hex_str = ''.join([f"{b:02x}" for b in sha512_hash])
    
    def get_even_chars(s):
        return ''.join([s[i] for i in range(1, len(s), 2)])
    
    def get_odd_chars(s):
        return ''.join([s[i] for i in range(0, len(s), 2)])
    
    processed_str = get_odd_chars(get_even_chars(hex_str))
    
    import hashlib
    md5_hash = hashlib.md5(processed_str.encode('utf-8')).digest()
    signature = ''.join([f"{b:02x}" for b in md5_hash]).upper()
    
    return signature

def generate_random_key(length=16):
    import random
    import string
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def rsa_encrypt(key, public_key, exponent):
    pub_key = rsa.PublicKey(int(public_key), int(exponent))
    encrypted = rsa.encrypt(key.encode('utf-8'), pub_key)
    return base64.b64encode(encrypted).decode('utf-8')

def aes_encrypt(data, key, iv):
    cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv.encode('utf-8'))
    padded_data = pad(data.encode('utf-8'), AES.block_size)
    encrypted = cipher.encrypt(padded_data)
    return base64.b64encode(encrypted).decode('utf-8')

def login(phone, password):
    import requests
    import logging
    
    logging.basicConfig(level=logging.DEBUG)
    
    timestamp = str(int(time.time() * 1000))
    
    params = {
        'phone': phone,
        'password': password,
        'j0': timestamp
    }
    
    params['i0'] = generate_signature(params)
    
    tree_map = dict(sorted(params.items()))
    
    random_key = generate_random_key()
    
    encrypted_key = rsa_encrypt(random_key, RSA_PUBLIC_KEY, RSA_EXPONENT)
    
    param_str = json.dumps(tree_map, ensure_ascii=False, separators=(',', ':'))
    
    encrypted_data = aes_encrypt(param_str, random_key, AES_IV)
    
    final_data = encrypted_data + ' ' + encrypted_key
    
    d_param = base64.b64encode(final_data.encode('utf-8')).decode('utf-8')
    
    request_data = {
        'd': d_param
    }
    
    url = 'https://appdmkj.5idream.net/v2/login/phone'
    
    headers = {
        'User-Agent': 'okhttp/3.11.0',
        'Content-Type': 'application/x-www-form-urlencoded',
        'standardua': '{"channelName":"dmkj_Android","countryCode":"CN","createTime":1758276123868,"device":"google Pixel 4","hardware":"flame","jPushId":"1507bfd3f6ff69d8819","modifyTime":1758276123868,"operator":"%E6%9C%AA%E7%9F%A5","screenResolution":"1080-2236","startTime":1758276471569,"sysVersion":"Android 29 10","system":"android","uuid":"2710bd5dee6e4ddd900fb5122cd8bb0d","version":"4.9.1"}',
    }
    
    print("\n=== 调试信息 ===")
    print(f"URL: {url}")
    print(f"Headers: {headers}")
    print(f"Request Data: {request_data}")
    print(f"原始参数: {params}")
    print(f"排序后参数: {tree_map}")
    print(f"参数字符串: {param_str}")
    print(f"随机密钥: {random_key}")
    print(f"加密后密钥: {encrypted_key}")
    print(f"加密后数据: {encrypted_data}")
    print(f"拼接后数据: {final_data}")
    print(f"d参数: {d_param}")
    print("================\n")
    
    try:
        response = requests.post(url, headers=headers, data=request_data, verify=False, timeout=10)
        print(f"响应状态码: {response.status_code}")
        print(f"响应头: {response.headers}")
        print(f"响应内容: {response.text}")
        return response.json()
    except Exception as e:
        print(f"请求异常: {e}")
        return {"error": str(e)}


if __name__ == '__main__':
    phone = '13699645879'
    password = 'Liux456123.'
    result = login(phone, password)
    print(result)
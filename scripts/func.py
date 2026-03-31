import hashlib
import random
import string
from sql.sql import search_for_existing_admin_key

def hash_in(thing_to_hash: str) -> str:
    h = hashlib.new('SHA512')
    h.update(bytes(thing_to_hash, encoding='utf-8'))
    return h.hexdigest()

def create_post_response(status:str = None, massage:str = None, url:str = None, cookie:str = None) -> dict:
    response = {
            'methods': 'POST',
            'headers': { 
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            'body': {
                'status': '',
                'massage': '',
                'url': '',
                'cookie': ''
            }
        }
    
    body = response['body']
    body['status'] = status
    body['massage'] = massage
    body['url'] = url
    body['cookie'] = cookie
    # print_in_file(f'create_post_response -- status: {response["body"]["status"]} \nmassage: {response["body"]["massage"]}')
    
    return response
    

def generate_confirmation_code(size=6, chars=string.ascii_letters + string.digits) -> str:
    return ''.join(random.choice(chars) for _ in range(size))

def create_key() -> str:
    key = generate_confirmation_code(30)
    ex_key, err = search_for_existing_admin_key(key)
    while len(ex_key) >= 2:
        key = generate_confirmation_code(30)
        ex_key, err = search_for_existing_admin_key(key)
    return key

def chech_for_lenth(item):
    if item.lenth() == 0:
        pass
    else:
        return item
import json
import random
import re
import sys
import threading
import time
from socket import socket, AF_INET, SOCK_STREAM

from backend_database import DataBase
from threadpool import ThreadPoolManager


def get_time() -> str:
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def get_reply_byte(reply: dict) -> bytes:
    return json.dumps(reply, ensure_ascii=False).encode(encoding='utf-8')


def print_error_message(message: str, reason: str) -> None:
    tid = threading.current_thread().name
    print(f'[{get_time()} {tid}] ERROR\t{message}: {reason}')


def print_ok_message(message: str) -> None:
    tid = threading.current_thread().name
    print(f'[{get_time()} {tid}] OK\t\t{message}')


def get_error_reply(data: dict, reason: str, message: str, content=None) -> bytes:
    print_error_message(message, reason)
    ans = {
        'type': data['type'],
        'data': {
            'status': 'error',
            'type': reason
        }
    }
    if content is not None:
        ans['data']['content'] = content
    return get_reply_byte(ans)


def get_ok_reply(data: dict, message: str, content=None) -> bytes:
    print_ok_message(message)
    ans = {
        'type': data['type'],
        'data': {
            'status': 'ok',
            'type': data['type']
        }
    }
    if content is not None:
        ans['data']['content'] = content
    return get_reply_byte(ans)


def is_user_exist(db: DataBase, uid: str) -> bool:
    return db.get_user_info(uid) != {}


def is_book_exist(db: DataBase, b_id: int) -> bool:
    return db.get_book_single(b_id) != {}


def is_bookmark_exist(db: DataBase, bm_id: int) -> bool:
    return db.get_bookmark_single(bm_id) != {}


def is_chapter_exist(db: DataBase, b_id: int, chap_id: int) -> bool:
    return db.get_chapter_single(b_id, chap_id) is not None


def handle_register(db: DataBase, data: dict) -> bytes:
    uid, psw, email = data['data']['uid'], data['data']['psw'], data['data']['email']
    message = f'TYPE={data["type"]} (uid, psw, email)=({uid}, {psw}, {email})'
    if psw in {None, ''}:
        reason = 'password cannot be null'
        return get_error_reply(data, reason, message)
    flag = db.add_user(uid, psw, email)
    if not flag:
        reason = 'user exist'
        return get_error_reply(data, reason, message)
    return get_ok_reply(data, message)


def handle_login(db: DataBase, data: dict) -> bytes:
    uid, psw = data['data']['uid'], data['data']['psw']
    message = f'TYPE={data["type"]} (uid, psw)=({uid}, {psw})'
    log_state = db.get_user_info(uid).get('log_state')
    if log_state is None:
        reason = 'user not exist'
        return get_error_reply(data, reason, message)
    if log_state == 1:
        reason = 'already login'
        return get_error_reply(data, reason, message)
    if not db.verify_user(uid, psw):
        reason = 'wrong password'
        return get_error_reply(data, reason, message)
    db.toggle_user_log_state(uid)
    return get_ok_reply(data, message)


def handle_logout(db: DataBase, data: dict) -> bytes:
    uid = data['data']['uid']
    message = f'TYPE={data["type"]} uid={uid}'
    log_state = db.get_user_info(uid).get('log_state')
    if log_state is None:
        reason = 'user not exist'
        return get_error_reply(data, reason, message)
    if log_state == 0:
        reason = 'already logout'
        return get_error_reply(data, reason, message)
    db.toggle_user_log_state(uid)
    return get_ok_reply(data, message)


def handle_get_chapter_single(db: DataBase, data: dict) -> bytes:
    b_id, chap_id = data['data']['book_id'], data['data']['chapter_id']
    message = f'TYPE={data["type"]} (book_id, chapter_id)=({b_id}, {chap_id})'
    if not is_book_exist(db, b_id):
        reason = 'book not exist'
        return get_error_reply(data, reason, message, [-1, ''])
    chap_str = db.get_chapter_single(b_id, chap_id)
    if chap_str is None:
        reason = 'chapter not exist'
        return get_error_reply(data, reason, message, [-1, ''])
    return get_ok_reply(data, message, [chap_id, chap_str])


def handle_get_chapter_all(db: DataBase, data: dict) -> bytes:
    b_id = data['data']['book_id']
    message = f'TYPE={data["type"]} book_id={b_id}'
    if not is_book_exist(db, b_id):
        reason = 'book not exist'
        return get_error_reply(data, reason, message, [])
    chap_list = db.get_chapter_all(b_id)
    return get_ok_reply(data, message, chap_list)


def handle_get_chapter_simple(db: DataBase, data: dict) -> bytes:
    b_id = data['data']['book_id']
    message = f'TYPE={data["type"]} book_id={b_id}'
    if not is_book_exist(db, b_id):
        reason = 'book not exist'
        return get_error_reply(data, reason, message, [])
    chap_list = db.get_chapter_simple(b_id)
    return get_ok_reply(data, message, chap_list)


def handle_get_bookmark_single(db: DataBase, data: dict) -> bytes:
    bm_id = data['data']['bookmark_id']
    message = f'TYPE={data["type"]} bookmark_id={bm_id}'
    bookmark = db.get_bookmark_single(bm_id)
    if bookmark == {}:
        reason = 'bookmark not exist'
        return get_error_reply(data, reason, message, bookmark)
    return get_ok_reply(data, message, bookmark)


def handle_get_bookmark_user(db: DataBase, data: dict) -> bytes:
    uid = data['data']['uid']
    message = f'TYPE={data["type"]} uid={uid}'
    if not is_user_exist(db, uid):
        reason = 'user not exist'
        return get_error_reply(data, reason, message, [])
    bookmark_list = db.get_bookmark_user(uid)
    return get_ok_reply(data, message, bookmark_list)


def handle_get_bookmark_user_book(db: DataBase, data: dict) -> bytes:
    uid, b_id = data['data']['uid'], data['data']['book_id']
    message = f'TYPE={data["type"]} (uid, book_id)=({uid}, {b_id})'
    if not is_user_exist(db, uid):
        reason = 'user not exist'
        return get_error_reply(data, reason, message, [])
    if not is_book_exist(db, b_id):
        reason = 'book not exist'
        return get_error_reply(data, reason, message, [])
    bookmark_list = db.get_bookmark_user_book(uid, b_id)
    return get_ok_reply(data, message, bookmark_list)


def handle_get_book_single(db: DataBase, data: dict) -> bytes:
    b_id = data['data']['book_id']
    message = f'TYPE={data["type"]} book_id={b_id}'
    book = db.get_book_single(b_id)
    if book == {}:
        reason = 'book not exist'
        return get_error_reply(data, reason, message, {})
    return get_ok_reply(data, message, book)


def handle_get_book_all(db: DataBase, data: dict) -> bytes:
    message = f'TYPE={data["type"]}'
    book_list = db.get_book_all()
    return get_ok_reply(data, message, book_list)


def handle_del_bookmark_single(db: DataBase, data: dict) -> bytes:
    bm_id = data['data']['bookmark_id']
    message = f'TYPE={data["type"]} bookmark_id={bm_id}'
    if not is_bookmark_exist(db, bm_id):
        reason = 'bookmark not exist'
        return get_error_reply(data, reason, message)
    db.del_bookmark_single(bm_id)
    return get_ok_reply(data, message)


def handle_del_bookmark_user(db: DataBase, data: dict) -> bytes:
    uid = data['data']['uid']
    message = f'TYPE={data["type"]} uid={uid}'
    if not is_user_exist(db, uid):
        reason = 'user not exist'
        return get_error_reply(data, reason, message)
    db.del_bookmark_user(uid)
    return get_ok_reply(data, message)


def handle_del_bookmark_user_book(db: DataBase, data: dict) -> bytes:
    uid, b_id = data['data']['uid'], data['data']['book_id']
    message = f'TYPE={data["type"]} (uid, book_id)=({uid}, {b_id})'
    if not is_user_exist(db, uid):
        reason = 'user not exist'
        return get_error_reply(data, reason, message)
    if not is_book_exist(db, b_id):
        reason = 'book not exist'
        return get_error_reply(data, reason, message)
    db.del_bookmark_user_book(uid, b_id)
    return get_ok_reply(data, message)


def handle_change_psw(db: DataBase, data: dict) -> bytes:
    uid, old_psw, new_psw = data['data']['uid'], data['data']['old_psw'], data['data']['new_psw']
    message = f'TYPE={data["type"]} (uid, old_psw, new_psw)=({uid}, {old_psw}, {new_psw})'
    if not is_user_exist(db, uid):
        reason = 'user not exist'
        return get_error_reply(data, reason, message)
    if not db.verify_user(uid, old_psw):
        reason = 'wrong password'
        return get_error_reply(data, reason, message)
    if old_psw == new_psw:
        reason = 'same password'
        return get_error_reply(data, reason, message)
    db.set_user_psw(uid, new_psw)
    return get_ok_reply(data, message)


def handle_add_bookmark(db: DataBase, data: dict) -> bytes:
    uid, b_id = data['data']['uid'], data['data']['book_id']
    bm_id, name = data['data']['bookmark_id'], data['data']['name']
    chap_id, page_num = data['data']['chapter_id'], data['data']['page_num']
    message = f'TYPE={data["type"]} (uid, book_id, bookmark_id, name, chapter_id, page_num)' \
              f'=({uid}, {b_id}, {bm_id}, {name}, {chap_id}, {page_num})'
    if not is_user_exist(db, uid):
        reason = 'user not exist'
        return get_error_reply(data, reason, message)
    if not is_book_exist(db, b_id):
        reason = 'book not exist'
        return get_error_reply(data, reason, message)
    if not is_chapter_exist(db, b_id, chap_id):
        reason = 'chapter not exist'
        return get_error_reply(data, reason, message)
    if is_bookmark_exist(db, bm_id):
        reason = 'bookmark exist'
        return get_error_reply(data, reason, message)
    db.add_bookmark(uid, b_id, bm_id, chap_id, page_num, name)
    return get_ok_reply(data, message)


def handle_get_bookmark_id(db: DataBase, data: dict) -> bytes:
    message = f'TYPE={data["type"]}'
    bookmark_id_set = set(db.get_bookmark_simple())
    total_set = {i for i in range(1, 65536)}
    ans_list = list(total_set - bookmark_id_set)
    if ans_list == []:
        reason = 'Bookmark ID number full'
        return get_error_reply(data, reason, message)
    else:
        content = random.choice(ans_list)
        return get_ok_reply(data, message, content)


switch = {
    'register': handle_register,
    'logout': handle_logout,
    'login': handle_login,
    'get_chapter_single': handle_get_chapter_single,
    'get_chapter_all': handle_get_chapter_all,
    'get_chapter_simple': handle_get_chapter_simple,
    'get_bookmark_single': handle_get_bookmark_single,
    'get_bookmark_user': handle_get_bookmark_user,
    'get_bookmark_user_book': handle_get_bookmark_user_book,
    'get_bookmark_id': handle_get_bookmark_id,
    'get_book_single': handle_get_book_single,
    'get_book_all': handle_get_book_all,
    'del_bookmark_single': handle_del_bookmark_single,
    'del_bookmark_user': handle_del_bookmark_user,
    'del_bookmark_user_book': handle_del_bookmark_user_book,
    'change_psw': handle_change_psw,
    'add_bookmark': handle_add_bookmark
}


def handle_type_not_exist(data: dict) -> bytes:
    message = f'TYPE=error data={data}'
    reason = 'type not exist'
    return get_error_reply({'type': 'error'}, reason, message)


def handle_type_illegal(data: dict) -> bytes:
    message = f'TYPE=default data={data}'
    reason = 'type illegal'
    return get_error_reply({'type': 'error'}, reason, message)


def handle_request(conn_socket: socket) -> None:
    recv_data = str(conn_socket.recv(1024), encoding='utf-8')

    data = json.loads(recv_data)
    if 'type' not in data:
        reply = handle_type_not_exist(data)
    elif data['type'] not in switch:
        reply = handle_type_illegal(data)
    else:
        db = DataBase()
        reply = switch[data['type']](db, data)

    conn_socket.send(reply)
    conn_socket.close()


def start_server(server_addr: str, server_port: int, max_conn_num: int, thread_num: int) -> None:
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind((server_addr, server_port))
    server_socket.listen(max_conn_num)
    welcome_statement = f'{get_time()}\nSimple Reader Server version 1.0\n' \
                        f'Starting server at {server_addr}:{server_port}, with max connection {max_conn_num} '
    print(welcome_statement)
    thread_pool = ThreadPoolManager(thread_num)
    while True:
        conn_socket, client_addr = server_socket.accept()
        thread_pool.add_job(handle_request, *(conn_socket,))


def ip_checker(addr):
    ip_compiler = re.compile('^(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|'
                             '2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)$')
    return ip_compiler.match(addr)


def port_checker(port):
    try:
        port_int = int(port)
    except:
        return False
    if port_int >= 0 and port_int <= 65535:
        return True
    else:
        return False


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Argument length is too short.')
        sys.exit(-1)
    else:
        addr, port = sys.argv[1], sys.argv[2]
        if not (ip_checker(addr) and port_checker(port)):
            print('Invalid IP address or IP port.')
            sys.exit(-1)
    start_server(addr, int(port), max_conn_num=5, thread_num=4)

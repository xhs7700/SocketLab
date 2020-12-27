import json
import sqlite3
from hashlib import sha256


class DataBase:
    def __init__(self):
        self.conn = sqlite3.connect('backend.db')
        # create users
        self.__create_table__('''
            create table users(
                uid varchar(255) primary key not null,
                psw varchar(128) not null,
                email varchar(255),
                log_state int not null
            );
        ''')
        # create bookmarks
        self.__create_table__('''
            create table bookmarks(
                bookmark_id int primary key not null,
                uid varchar(255) not null,
                book_id int not null,
                name varchar(255) not null,
                chapter_id int not null,
                page_num int not null
            );
        ''')
        # create books
        self.__create_table__('''
            create table books(
                book_id int primary key not null,
                path varchar(255) not null,
                name varchar(255) not null
            );
        ''')
        # create chapters
        self.__create_table__('''
            create table chapters(
                book_id int not null,
                chapter_id int not null,
                path varchar(255) not null,
                primary key (book_id,chapter_id)
            )
        ''')

    def __create_table__(self, statement: str) -> None:
        try:
            self.conn.execute(statement)
        except sqlite3.OperationalError:
            pass

    def __safe_change__(self, statement: str) -> bool:
        try:
            self.conn.execute(statement)
            self.conn.commit()
            return True
        except:
            self.conn.rollback()
            return False

    def __get_user_info__(self, uid: str) -> dict:
        statement = f'select psw,uid,email,log_state from users where uid="{uid}";'
        cur = self.conn.cursor()
        cur.execute(statement)
        ans = cur.fetchone()
        if ans is not None:
            return get_query_as_dict(cur, ans)
        else:
            return {}

    def add_user(self, uid: str, psw: str, email: str) -> bool:
        statement = get_add_user_statement(email, psw, uid)
        return self.__safe_change__(statement)

    def get_user_info(self, uid: str) -> dict:
        ans = self.__get_user_info__(uid)
        if 'psw' in ans:
            ans.pop('psw')
        return ans

    def toggle_user_log_state(self, uid: str) -> bool:
        statement = f'update users set log_state=1-log_state where uid="{uid}";'
        return self.__safe_change__(statement)

    def set_user_email(self, uid: str, email: str) -> bool:
        statement = f'update users set email="{email}" where uid="{uid}";'
        return self.__safe_change__(statement)

    def set_user_psw(self, uid: str, psw: str) -> bool:
        real_psw = encrypt_password(psw, uid)
        statement = f'update users set psw="{real_psw}" where uid="{uid}";'
        return self.__safe_change__(statement)

    def verify_user(self, uid: str, verify_psw: str) -> bool:
        psw = self.__get_user_info__(uid).get('psw')
        if psw is None: return False
        verify_psw = encrypt_password(verify_psw, uid)
        return verify_psw == psw

    def add_bookmark(self, uid: str, b_id: int, bm_id: int, con_chapter: int, con_page: int, name: str) -> bool:
        statement = get_add_bookmark_statement(uid, b_id, bm_id, con_chapter, con_page, name)
        return self.__safe_change__(statement)

    def get_bookmark_single(self, bm_id: int) -> dict:
        statement = f'select uid,bookmark_id,book_id,chapter_id,page_num,name from bookmarks where bookmark_id={bm_id};'
        cur = self.conn.cursor()
        cur.execute(statement)
        ans = cur.fetchone()
        if ans is not None:
            return get_query_as_dict(cur, ans)
        else:
            return {}

    def get_bookmark_user(self, uid: str) -> list:
        statement = f'select bookmark_id,book_id,chapter_id,page_num,name from bookmarks where uid="{uid}";'
        cur = self.conn.cursor()
        cur.execute(statement)
        ans_list = cur.fetchall()
        return [get_query_as_dict(cur, ans) for ans in ans_list]

    def get_bookmark_user_book(self, uid: str, b_id: int) -> list:
        statement = f'select bookmark_id,chapter_id,page_num,name from bookmarks where uid="{uid}" and book_id={b_id};'
        cur = self.conn.cursor()
        cur.execute(statement)
        ans_list = cur.fetchall()
        return [get_query_as_dict(cur, ans) for ans in ans_list]

    def get_bookmark_simple(self) -> list:
        statement = f'select bookmark_id from bookmarks;'
        cur = self.conn.cursor()
        cur.execute(statement)
        ans_list = cur.fetchall()
        return [ans[0] for ans in ans_list]

    def del_bookmark_single(self, bm_id: int) -> bool:
        statement = f'delete from bookmarks where bookmark_id={bm_id};'
        return self.__safe_change__(statement)

    def del_bookmark_user(self, uid: str) -> bool:
        statement = f'delete from bookmarks where uid="{uid}";'
        return self.__safe_change__(statement)

    def del_bookmark_user_book(self, uid: str, b_id: int) -> bool:
        statement = f'delete from bookmarks where uid="{uid}" and book_id={b_id};'
        return self.__safe_change__(statement)

    def get_book_single(self, b_id: int) -> dict:
        statement = f'select book_id,name from books where book_id={b_id};'
        cur = self.conn.cursor()
        cur.execute(statement)
        ans = cur.fetchone()
        if ans is not None:
            return get_query_as_dict(cur, ans)
        else:
            return {}

    def get_book_all(self) -> list:
        statement = f'select book_id,name from books;'
        cur = self.conn.cursor()
        cur.execute(statement)
        ans_list = cur.fetchall()
        return [get_query_as_dict(cur, ans) for ans in ans_list]

    def get_chapter_single(self, b_id: int, chap_id: int) -> object:
        statement = f'select path from chapters where book_id={b_id} and chapter_id={chap_id}; '
        cur = self.conn.cursor()
        cur.execute(statement)
        ans = cur.fetchone()
        if ans is not None:
            with open(ans[0], 'r', encoding='utf-8') as fp:
                chap_str = fp.read()
            return chap_str
        else:
            return None

    def get_chapter_all(self, b_id: int) -> list:
        statement = f'select chapter_id, path from chapters where book_id={b_id};'
        cur = self.conn.cursor()
        cur.execute(statement)
        ans = cur.fetchall()
        chap_list = []
        for chap_id, path in ans:
            with open(path, 'r', encoding='utf-8') as fp:
                chap_str = fp.read()
            chap_list.append((chap_id, chap_str))
        return chap_list

    def get_chapter_simple(self, b_id: int) -> list:
        statement = f'select chapter_id from chapters where book_id={b_id};'
        cur = self.conn.cursor()
        cur.execute(statement)
        ans_list = cur.fetchall()
        return [ans[0] for ans in ans_list]

    def close(self):
        self.conn.close()


def get_query_as_dict(cur, ans: tuple) -> dict:
    return {x[0]: ans[i] for i, x in enumerate(cur.description)}


def safe_execute(conn: sqlite3.Connection, statement: str) -> bool:
    # conn.execute(statement)
    # conn.commit()
    try:
        conn.execute(statement)
        conn.commit()
        return True
    except:
        # print("Wrong Execute.")
        conn.rollback()
        return False


def inject_book_data():
    conn = sqlite3.connect('backend.db')
    with open('books.json', 'r', encoding='utf-8') as f:
        # data_str=f.read()
        data = json.load(f)
        books = data['books']
    for book in books:
        uid, name, path = book['id'], book['name'], book['path']
        statement = f'''
            insert into books (book_id,path,name)
            values ({uid},"{path}","{name}");
        '''
        # print(statement)
        safe_execute(conn, statement)
        for chapter in book['chapters']:
            chapter_id = chapter['id']
            chapter_path = path + f'\\{name}_{chapter_id}.txt'
            chapter_statement = f'''
                insert into chapters(book_id,chapter_id,path)
                values ({uid},{chapter_id},"{chapter_path}");
            '''
            safe_execute(conn, chapter_statement)
    conn.close()


def inject_user_data():
    conn = sqlite3.connect('backend.db')
    with open('users.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        users = data['users']
    for user in users:
        uid, psw, email = user['id'], user['psw'], user['email']
        statement = get_add_user_statement(email, psw, uid)
        safe_execute(conn, statement)
    conn.close()


def get_add_bookmark_statement(uid: str, b_id: int, bm_id: int, con_chapter: int, con_page: int, name: str) -> str:
    statement = f'''
        insert into bookmarks(uid,bookmark_id,book_id,chapter_id,page_num,name)
        values ("{uid}",{bm_id},{b_id},{con_chapter},{con_page},"{name}");
    '''
    return statement


def get_add_user_statement(email: str, psw: str, uid: str) -> str:
    frag = 'null' if email in {'', None} else f'"{email}"'
    psw = encrypt_password(psw, uid)
    statement = f'''
            insert into users(uid,psw,email,log_state)
            values ("{uid}","{psw}",{frag},0);
        '''
    return statement


def encrypt_password(psw: str, uid: str) -> str:
    hsh = sha256()
    tmp = uid + psw
    hsh.update(tmp.encode('utf-8'))
    psw = hsh.hexdigest()
    return psw


if __name__ == '__main__':
    db = DataBase()
    print(db.get_user_info('xhs7700'))
    db.close()

import json
import os
from socket import socket, AF_INET, SOCK_STREAM


def check_by_path(path):
    with open(path, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)
        query_list = []
        if 'examples' in raw_data:
            query_list = raw_data['examples']
        else:
            query_list = [raw_data]
    for query in query_list:
        print(socket_send(query))


def socket_send(query):
    server_name, server_port = '45.134.171.215', 6370
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((server_name, server_port))
    query_byte = json.dumps(query, ensure_ascii=False).encode(encoding='utf-8')
    client_socket.send(query_byte)
    recv_data = client_socket.recv(1024 * 1024).decode(encoding='utf-8')
    # print(recv_data.decode(encoding='utf-8'))
    client_socket.close()
    return recv_data


if __name__ == '__main__':

    root_path = os.path.join(os.getcwd(), 'protocol_example')
    path_list = []
    for sub_path in os.listdir(root_path):
        if sub_path.endswith('_server.json'): continue
        path_list.append(os.path.join(root_path, sub_path))
    for path in path_list:
        check_by_path(path)

import sys
sys.path.append("..")
import os
from common import SERVER_HOST, SERVER_PORT
import http.client
import json

class Client:
    def __init__(self, server_host = SERVER_HOST, server_port = SERVER_PORT):
        self.conn = http.client.HTTPConnection(server_host, server_port)
    
    def __del__(self):
        pass
    
    def login(self, username, passwd):
        request_headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        request_body = "username=%s&passwd=%s"%(username,passwd)

        self.conn.request("POST", "/login", body = request_body, headers = request_headers)
        response = self.conn.getresponse()
        user_info = json.loads(response.read())
        
        return user_info


    def register(self, username, passwd):
        request_headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        request_body = "username=%s&passwd=%s"%(username,passwd)

        self.conn.request("POST", "/register", body = request_body, headers = request_headers)
        response = self.conn.getresponse()
        user_info = json.loads(response.read())
        
        return user_info

    def update(self, username, passwd, d_total, d_wins):
        request_headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        request_body = "username=%s&passwd=%s&d_total=%s&d_wins=%s"%(username,passwd,d_total,d_wins)

        self.conn.request("POST", "/update", body = request_body, headers = request_headers)
        response = self.conn.getresponse()
        user_info = json.loads(response.read())
        
        return user_info
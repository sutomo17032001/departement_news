import json
from unittest import result
from xml.etree.ElementTree import tostring

from nameko.rpc import RpcProxy
from nameko.web.handlers import http
from werkzeug.wrappers import Response
from session import SessionProvider

class GatewayService:
    name = 'gateway'

    database = RpcProxy('user_service')
    session_provider = SessionProvider()
    
    @http('POST', '/regis')
    def regis(self, request):
        data = format(request.get_data(as_text=True))
        arr  =  data.split("&")

        username = "" 
        password = "" 
        for el in arr:
            node = el.split("=")
            if node[0] == "username":
                username = node[1]
            if node[0] == "password":
                password = node[1]
        rooms = self.database.regis(username, password)
        return json.dumps(rooms)

    @http('GET', '/login')
    def login(self, request):
        data = format(request.get_data(as_text=True))
        arr  =  data.split("&")

        username = "" 
        password = "" 
        for el in arr:
            node = el.split("=")
            if node[0] == "username":
                username = node[1]
            if node[0] == "password":
                password = node[1]
        flags = self.database.login(username, password)
        
        if(flags == 1):
            user_data = {
                'username': username,
                'password': password
            }
            session_id = self.session_provider.set_session(user_data)
            response = Response(str(user_data))
            response.set_cookie('SESSID', session_id)
            return response
        else:
            result = []
            result.append("Username/password incorrect")
            return json.dumps(result)
    
    @http('GET', '/get_all_news')
    def get_all_news(self, request):
        news = self.database.get_all_news()
        return json.dumps(news)
    
    @http('GET', '/get_news_id/<int:id>')
    def get_news_id(self, request, id):
        news = self.database.get_news_id(id)
        return json.dumps(news)

    @http('POST', '/add_news')
    def add_news(self, request):
        cookies = request.cookies
        if cookies:
            data = format(request.get_data(as_text=True))
            arr = data.split("&")

            judul = ""
            isi_berita = ""
            for el in arr:
                node = el.split("=")
                if node[0] == "judul":
                    judul = node[1]
                if node[0] == "isi_berita":
                    isi_berita = node[1]
            news = self.database.add_news(judul, isi_berita)
            return json.dumps(news)
        else:
            result = []
            result.append("Login Required")
            return json.dumps(result)

    @http('DELETE', '/delete_news_id/<int:id>')
    def delete_news_id(self, request, id):
        cookies = request.cookies
        if cookies:
            news = self.database.delete_news_id(id)
            return json.dumps(news)
        else:
            result = []
            result.append("Login Required")
            return json.dumps(result)

    @http('PUT', '/edit_news/<int:id>')
    def edit_news(self, request, id):
        cookies = request.cookies
        if cookies:
            req = request.json
            judul = req["judul"]
            news = self.database.edit_news(id, judul)
            return int(news['status_code']), (json.dumps(news['response'], indent=4))
        else:
            result = []
            result.append("Login Required")
            return json.dumps(result)

    @http('GET', '/check')
    def check(self, request):
        cookies = request.cookies
        return Response(cookies['SESSID'])
    
    @http('GET', 'user/logout')
    def logout(self, request):
        hasil = {'message':"Error"}
        cookies = request.cookies
        if cookies:
            hasil['message'] = "user logged out successfully"
            res = self.session_provider.delete_session(cookies["SESSID"])
            response = Response(str(hasil))
            response.delete_cookie('SESSID')
        
        return response
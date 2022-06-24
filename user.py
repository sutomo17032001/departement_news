from nameko.rpc import rpc

import dependencies

class UserService:

    name = 'user_service'

    database = dependencies.Database()

    @rpc
    def regis(self, username, password):
        user = self.database.regis(username, password)
        return user
    
    @rpc
    def login(self, username, password):
        user = self.database.login(username, password)
        return user

    @rpc
    def get_all_news(self):
        news = self.database.get_all_news()
        return news
    
    @rpc
    def get_news_id(self, id):
        news = self.database.get_news_id(id)
        return news
    
    @rpc
    def add_news(self, judul, isi_berita):
        news = self.database.add_news(judul, isi_berita)
        return news
    
    @rpc
    def delete_news_id(self, id):
        news = self.database.delete_news_id(id)
        return news
    
    @rpc
    def edit_news(self, id, judul):
        news = self.database.edit_news(id, judul)
        return news
    
    @rpc
    def logout(self):
        user = self.database.logout()
        return user

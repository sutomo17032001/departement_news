from sqlite3 import Cursor
from unittest import result
from nameko.extensions import DependencyProvider

import mysql.connector
from mysql.connector import Error
from mysql.connector import pooling
import itertools

class DatabaseWrapper:

    connection = None

    def __init__(self, connection):
        self.connection = connection

    def regis(self, username, password):
        cursor = self.connection.cursor(dictionary=True, buffered=True)
        result = []
        sql = "SELECT * from user where username = '{}'".format(username)
        cursor.execute(sql)
        if(cursor.rowcount > 0):
            cursor.close()
            result.append("Username telah terdaftar")
            return result
        else:
            sql = "INSERT INTO user VALUES(0, '{}', '{}')".format(username, password)
            cursor.execute(sql)
            self.connection.commit()
            cursor.close()
            result.append("Registrasi berhasil")
            return result
        
    def login(self, username, password):
        cursor = self.connection.cursor(dictionary=True, buffered=True)
        result = []
        sql = "SELECT * from user where username = '{}'".format(username)
        cursor.execute(sql)
        if(cursor.rowcount == 0):
            cursor.close()
            result.append("Username tidak terdaftar")
            return result
        else:
            resultfetch = cursor.fetchone()
            if(resultfetch['password'] == password):
                cursor.close()
                result.append("Login Berhasil")
                return result
            else:
                cursor.close()
                result.append("Password salah")
                return result

    def get_all_news(self):
        cursor = self.connection.cursor(dictionary=True)
        result = []
        sql = "SELECT * FROM berita"
        cursor.execute(sql)
        for row in cursor.fetchall():
            result.append({
                'id': row['id'],
                'judul': row['judul'],
                'isi_berita': row['isi_berita'],
            })
        cursor.close()
        return result

    def get_news_id(self, id):
        cursor = self.connection.cursor(dictionary=True)
        result = []
        sql = "SELECT * FROM berita WHERE id = {}".format(id)
        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.close()
        return result

    def add_news(self, judul, isi_berita):
        cursor = self.connection.cursor(dictionary=True, buffered=True)
        result = []
        sql = "SELECT * from berita where judul = '{}'".format(judul)
        cursor.execute(sql)
        if(cursor.rowcount >= 0):
            sql = "INSERT INTO berita VALUES(0, '{}', '{}')".format(judul, isi_berita)
            cursor.execute(sql)
            self.connection.commit()
            cursor.close()
            result.append("News berhasil ditambahkan")
            return result

    def delete_news_id(self, id):
        cursor = self.connection.cursor(dictionary=True)
        result = []
        sql = "DELETE FROM berita WHERE id = " + str(id)
        cursor.execute(sql)
        sql = "SELECT * FROM berita"
        cursor.execute(sql)
        for row in cursor.fetchall():
            result.append({
                'id': row['id'],
                'judul': row['judul'],
                'isi_berita': row['isi_berita'],
            })
        self.connection.commit()
        cursor.close()
        return result 

    def edit_news(self, id, judul):
        result = {}
        response = {}
        cursor = self.connection.cursor()
        sql = "SELECT * FROM berita WHERE id = %s"
        cursor.execute(sql, [int(id)])
        row = cursor.fetchall()
        row_count = cursor.rowcount

        if row_count == 1:
            cursor = self.connection.cursor()
            sql2 = "UPDATE berita SET judul = %s WHERE id = %s"
            cursor.execute(sql2, [judul, int(id)])
            self.connection.commit()

            sql3 = "SELECT * FROM berita WHERE judul = %s AND id = %s"
            cursor.execute(sql3, [judul, int(id)])
            row = cursor.fetchone()
            data = {"id": row[0], "judul": row[1],
                    "isi": row[2]}
            response['status'] = 'success'
            response['message'] = 'news updated successfully'
            response['data'] = data
            result['status_code'] = 200
        else:
            response['status'] = 'error'
            response['message'] = 'news not found'
            result['status_code'] = 404

class Database(DependencyProvider):

    connection_pool = None

    def __init__(self):
        try:
            self.connection_pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name="database_pool",
                pool_size=5,
                pool_reset_session=True,
                host='localhost',
                database='news',
                user='root',
                password=''
            )
        except Error as e :
            print ("Error while connecting to MySQL using Connection pool ", e)

    def get_dependency(self, worker_ctx):
        return DatabaseWrapper(self.connection_pool.get_connection())

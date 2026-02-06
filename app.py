from flask import Flask, jsonify
import sqlite3
import time

class Server():
    def __init__(self):
        self.server = Flask(__name__)
        self.database = Database()
        self.sayfalar()

    def sayfalar(self):
        @self.server.route("/notyaz/<string:Not>/<string:Yazan>")
        def home(Not,Yazan):
            self.database.not_ekle(Not,time.strftime("%Y-%m-%d %H:%M:%S"),Yazan)
            return jsonify({"Durum":"Not Eklendi"})
        
        @self.server.route("/notlar/<string:Yazan>")
        def notlar(Yazan):
            Notlar = self.database.not_yazdir(Yazan)
            return jsonify(Notlar)

class Database():
    def __init__(self):
        with sqlite3.connect("Database.db") as baglanti:
            cursor = baglanti.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS Notlar (Notlar TEXT, Tarih TEXT, Yazan TEXT)")
            baglanti.commit()

    def not_ekle(self,Not,Tarih,Yazan):
        with sqlite3.connect("Database.db") as baglanti:
            cursor = baglanti.cursor()
            cursor.execute("INSERT INTO Notlar VALUES (?,?,?)",(Not,Tarih,Yazan))
            baglanti.commit()

    def not_yazdir(self,Yazan):
        with sqlite3.connect("Database.db") as baglanti:
            cursor = baglanti.cursor()
            cursor.execute("SELECT * FROM Notlar WHERE Yazan = ?",(Yazan,))
            YazanDB = cursor.fetchall()

            if YazanDB:
                return YazanDB
            else:
                return {"Durum":"Not Bulunamadi"}

if __name__ == "__main__":
    Server().server.run(debug=True)

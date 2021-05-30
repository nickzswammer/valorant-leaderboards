import json
import requests
from flask import render_template, Blueprint
from flask import Flask, redirect, url_for, request
from dotenv import load_dotenv
import os
import mysql.connector
from flaskext.mysql import MySQL

#Create App
app = Flask(__name__)


#Environment Variable API_KEY
load_dotenv()
API_KEY = os.getenv('API_KEY')
PASS = os.getenv('PASSWORD')

#API Response

#Connect with MySQL Database
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'sql3415644'
app.config['MYSQL_DATABASE_PASSWORD'] = PASS
app.config['MYSQL_DATABASE_DB'] = 'sql3415644'
app.config['MYSQL_DATABASE_HOST'] = 'sql3.freemysqlhosting.net'
mysql.init_app(app)

connection = mysql.connect()
cursor = connection.cursor()


#Create Routes
@app.route('/',  methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        act_id = request.form.get('acts')
        valorant = requests.get(f'https://na.api.riotgames.com/val/ranked/v1/leaderboards/by-act/{act_id}?size=200&startIndex=0&api_key={API_KEY}')
        print(act_id)
        top = request.form['top']
        act_num = ''

        if act_id == '97b6e739-44cc-ffa7-49ad-398ba502ceb0':
            act_num = '1'
        elif act_id == 'ab57ef51-4e59-da91-cc8d-51a5a2b9b8ff':
            act_num = '2'
        else:
            act_num='3'

    
        players = []

        for i in range(int(top)):
            try:
                players.append((i+1, valorant.json()['players'][i]['gameName'], valorant.json()['players'][i]['rankedRating'], valorant.json()['players'][i]['numberOfWins']))
                
            except:
                print("Invalid Data")

        return render_template('index.html', top=f'Currently showing top {top} players', players=players, act_num=f'of ACT {act_num}')
    return render_template('index.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        insertdatabase = 'INSERT INTO users (name, email, message) VALUES (%s, %s, %s)'
        inputs = (name, email, message)

        cursor.execute(insertdatabase, inputs)
        connection.commit()

        return render_template('contact.html', success_message = "Message sent successfully. I will reach out to you shortly.")

    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
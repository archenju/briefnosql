#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask
from flask import request
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client['flashbot']
collec = db['jobsearch']  

@app.route('/')
def root():
    return '''
        <html><head></head><body>
            <div style="width:800px; margin:0 auto;">
            <h1><i>Monsieur Pontier International, Inc.</i></h1>
            <br><form action="/search" method="post">
            <div style="width:1600px; margin:0 auto;justify-content: center;">
                <br><input type=text name=query>
                <input type=submit value=search>
            </form><br></div></div>
        </body></html>
    '''

@app.route('/search', methods=['POST', 'GET'])
def search():
    rendered = '''
        <html><head></head><body>
            <h1>Monsieur Pontier International</h1>
            <form action="/search" method="post">
                <p><input type=text name=query placeholder="
    '''
    closeform = '''
        ">
        <input type=submit value=search><p>
    </form><br><br>
    '''
    closing = "</body></html>"
    if request.method == 'POST':
        searchquery = request.form['query']
        mongoresponse = collec.find( {"$text" : {"$search": searchquery}} )
        #mongoresponse = collec.find({"query": searchquery})
        htmlresponse = ""
        for resp in mongoresponse:
            htmlresponse = htmlresponse + "<br><b>" + resp['title'][0] + "</b><br>"
            htmlresponse = htmlresponse + resp['pubDate'][0] + "<br>"
            htmlresponse = htmlresponse + resp['description'][0] + "<br>"
            htmlresponse = htmlresponse + resp['link'][0] + "<br><br>"
        return rendered + searchquery + closeform + htmlresponse + closing
    else:
        return "GET!"

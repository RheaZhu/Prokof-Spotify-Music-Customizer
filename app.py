import os
import sqlite3
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from datetime import datetime
from dotenv import load_dotenv 
import base64
import requests
from requests import post, get
import json


#Load environment variables for Spotify API
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
db = SQL("sqlite:///spotify.db") 
db.execute( "CREATE TABLE IF NOT EXISTS tracks (name TEXT NOT NULL, artist TEXT NOT NULL, id TEXT NOT NULL UNIQUE)")

#Get tocken for Spotify API
def get_token():
    
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token" 
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data) 
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

#get header for Spotify API requests
def get_auth_header(token):
    return { "Authorization": "Bearer " + token, }

#Search for a track using Spotify API, for inputs
def search_for_trackid(token, track_name, artist_name):
    headers = get_auth_header(token) 
    params = {
        'q': f"track:{track_name} artist:{artist_name}",
        'type': 'track', 
        'limit': 1
    }

    response = get('https://api.spotify.com/v1/search', params=params, headers=headers) 
    json_result = json.loads(response.content)["tracks"]["items"][0]["id"]
    return json_result

def search_for_artist_id(token, artist_name):
    headers = get_auth_header(token) 
    params = {
        'q': f"artist:{artist_name}",
        'type': 'artist', 
        'limit': 1
    }

    response = get('https://api.spotify.com/v1/search', params=params, headers=headers) 
    json_result = json.loads(response.content)["artists"]["items"][0]["id"]
    return json_result

def most_popular_tracks(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?market=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    print(result.status_code, result.content)
    json_result = json.loads(result.content)["tracks"]
    return json_result

def get_albums(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/albums?include_groups=album,single&market=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["items"]
    return json_result

def get_tracks_from_album(token, album_id):
    url = f"https://api.spotify.com/v1/albums/{album_id}/tracks?market=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["items"]
    return json_result



# Create Flask application
app = Flask(__name__) 
token = get_token()
# Configure application
@app.route("/")
def homepage():
    return render_template("homepage.html")

@app.route("/instructions")
def instructions():
    return render_template("instructions.html")

@app.route("/function", methods=["GET", "POST"])
def function():
    if request.method == "GET":
        return render_template("function.html")
    else: 
        mode = request.form.get("mode")
        return redirect("/input?mode=" + mode)
    
@app.route("/database")
def database():
    return render_template("database.html")

@app.route("/input", methods=["GET", "POST"])
def input():
    if request.method == "GET":
        mode = request.args.get("mode")
        return render_template("input.html", mode=mode)
    else: 
        # Process the form data
        for i in range(1):
            input1 = request.form.get("input1")
            input1a = request.form.get("input1a")

            input2 = request.form.get("input2") 
            input2a = request.form.get("input2a")

            input3 = request.form.get("input3")
            input3a = request.form.get("input3a")
        
            input4 = request.form.get("input4")
            input4a = request.form.get("input4a")
            
            input5 = request.form.get("input5")
            input5a = request.form.get("input5a")
        mode = request.args.get("mode")
        return redirect("/mode" + mode + "?input1=" + input1 + "&input1a=" + input1a +
                        "&input2=" + input2 + "&input2a=" + input2a +
                        "&input3=" + input3 + "&input3a=" + input3a +
                        "&input4=" + input4 + "&input4a=" + input4a +
                        "&input5=" + input5 + "&input5a=" + input5a)

@app.route("/mode1", methods=["GET", "POST"])
def mode1():
    db.execute("DELETE FROM tracks")
    # Get inputs from URL parameters
    input1 = request.args.get("input1")
    input1a = request.args.get("input1a")
    input2 = request.args.get("input2") 
    input2a = request.args.get("input2a")
    input3 = request.args.get("input3")
    input3a = request.args.get("input3a")
    input4 = request.args.get("input4")
    input4a = request.args.get("input4a")    
    input5 = request.args.get("input5")
    input5a = request.args.get("input5a")
    

    # Get most popular tracks
    #if input1 and input1a:
    artist1 = search_for_artist_id(token, input1a)
    tracks1 = most_popular_tracks(token, artist1)
    count = 0
    for i in range(1):
        for track in tracks1: 
            db.execute("INSERT OR IGNORE INTO tracks (name, artist, id) VALUES (?, ?, ?)", track["name"], track["artists"][0]["name"], track["id"])
            count += 1
        albums = get_albums(token, artist1)
        for album in albums:
            tracks = get_tracks_from_album(token, album["id"])
            for track in tracks:
                db.execute("INSERT OR IGNORE INTO tracks (name, artist, id) VALUES (?, ?, ?)", track["name"], track["artists"][0]["name"], track["id"])
                count +=1 
                if count >= 50:
                    break
            if count >= 50:
                break
    
    if input2 and input2a:
        artist = search_for_artist_id(token, input2a)
        tracks = most_popular_tracks(token, artist)
        count = 0
        for i in range(1):
            for track in tracks: 
                db.execute("INSERT OR IGNORE INTO tracks (name, artist, id) VALUES (?, ?, ?)", track["name"], track["artists"][0]["name"], track["id"])
                count += 1
            albums = get_albums(token, artist)
            for album in albums:
                tracks = get_tracks_from_album(token, album["id"])
                for track in tracks:
                    db.execute("INSERT OR IGNORE INTO tracks (name, artist, id) VALUES (?, ?, ?)", track["name"], track["artists"][0]["name"], track["id"])
                    count +=1 
                    if count >= 50:
                        break
                if count >= 50:
                    break
    if input3 and input3a:
        artist = search_for_artist_id(token, input3a)
        tracks = most_popular_tracks(token, artist)
        count = 0
        for i in range(1):
            for track in tracks: 
                db.execute("INSERT OR IGNORE INTO tracks (name, artist, id) VALUES (?, ?, ?)", track["name"], track["artists"][0]["name"], track["id"])
                count += 1
            albums = get_albums(token, artist)
            for album in albums:
                tracks = get_tracks_from_album(token, album["id"])
                for track in tracks:
                    db.execute("INSERT OR IGNORE INTO tracks (name, artist, id) VALUES (?, ?, ?)", track["name"], track["artists"][0]["name"], track["id"])
                    count +=1 
                    if count >= 50:
                        break
                if count >= 50:
                    break 
    if input4 and input4a:
        artist = search_for_artist_id(token, input4a)
        tracks = most_popular_tracks(token, artist)
        count = 0
        for i in range(1):
            for track in tracks: 
                db.execute("INSERT OR IGNORE INTO tracks (name, artist, id) VALUES (?, ?, ?)", track["name"], track["artists"][0]["name"], track["id"])
                count += 1
            albums = get_albums(token, artist)
            for album in albums:
                tracks = get_tracks_from_album(token, album["id"])
                for track in tracks:
                    db.execute("INSERT OR IGNORE INTO tracks (name, artist, id) VALUES (?, ?, ?)", track["name"], track["artists"][0]["name"], track["id"])
                    count +=1 
                    if count >= 50:
                        break
                if count >= 50:
                    break
    if input5 and input5a:
        artist = search_for_artist_id(token, input5a)
        tracks = most_popular_tracks(token, artist)
        count = 0
        for i in range(1):
            for track in tracks: 
                db.execute("INSERT OR IGNORE INTO tracks (name, artist, id) VALUES (?, ?, ?)", track["name"], track["artists"][0]["name"], track["id"])
                count += 1
            albums = get_albums(token, artist)
            for album in albums:
                tracks = get_tracks_from_album(token, album["id"])
                for track in tracks:
                    db.execute("INSERT OR IGNORE INTO tracks (name, artist, id) VALUES (?, ?, ?)", track["name"], track["artists"][0]["name"], track["id"])
                    count +=1 
                    if count >= 50:
                        break
                if count >= 50:
                    break
    songs = db.execute("SELECT * FROM tracks ORDER BY RANDOM() LIMIT 50") 
    return render_template("mode1.html", songs=songs)
@app.route("/mode2")
def mode2():
    db.execute("DELETE FROM tracks")
    # Get inputs from URL parameters
    input1 = request.args.get("input1")
    input1a = request.args.get("input1a")
    input2 = request.args.get("input2") 
    input2a = request.args.get("input2a")
    input3 = request.args.get("input3")
    input3a = request.args.get("input3a")
    input4 = request.args.get("input4")
    input4a = request.args.get("input4a")    
    input5 = request.args.get("input5")
    input5a = request.args.get("input5a")
    

    # Get most popular tracks
    #if input1 and input1a:
    artist1 = search_for_artist_id(token, input1a)
    tracks1 = most_popular_tracks(token, artist1)
    count = 0
    for i in range(1):
        for track in tracks1: 
            db.execute("INSERT OR IGNORE INTO tracks (name, artist, id) VALUES (?, ?, ?)", track["name"], track["artists"][0]["name"], track["id"])
            count += 1
        albums = get_albums(token, artist1)
        for album in albums:
            tracks = get_tracks_from_album(token, album["id"])
            for track in tracks:
                db.execute("INSERT OR IGNORE INTO tracks (name, artist, id) VALUES (?, ?, ?)", track["name"], track["artists"][0]["name"], track["id"])
                count +=1 
                if count >= 20:
                    break
            if count >= 20:
                break
    
    if input2 and input2a:
        artist = search_for_artist_id(token, input2a)
        tracks = most_popular_tracks(token, artist)
        count = 0
        for i in range(1):
            for track in tracks: 
                db.execute("INSERT OR IGNORE INTO tracks (name, artist, id) VALUES (?, ?, ?)", track["name"], track["artists"][0]["name"], track["id"])
                count += 1
            albums = get_albums(token, artist)
            for album in albums:
                tracks = get_tracks_from_album(token, album["id"])
                for track in tracks:
                    db.execute("INSERT OR IGNORE INTO tracks (name, artist, id) VALUES (?, ?, ?)", track["name"], track["artists"][0]["name"], track["id"])
                    count +=1 
                    if count >= 20:
                        break
                if count >= 20:
                    break
    if input3 and input3a:
        artist = search_for_artist_id(token, input3a)
        tracks = most_popular_tracks(token, artist)
        count = 0
        for i in range(1):
            for track in tracks: 
                db.execute("INSERT OR IGNORE INTO tracks (name, artist, id) VALUES (?, ?, ?)", track["name"], track["artists"][0]["name"], track["id"])
                count += 1
            albums = get_albums(token, artist)
            for album in albums:
                tracks = get_tracks_from_album(token, album["id"])
                for track in tracks:
                    db.execute("INSERT OR IGNORE INTO tracks (name, artist, id) VALUES (?, ?, ?)", track["name"], track["artists"][0]["name"], track["id"])
                    count +=1 
                    if count >= 20:
                        break
                if count >= 20:
                    break 
    if input4 and input4a:
        artist = search_for_artist_id(token, input4a)
        tracks = most_popular_tracks(token, artist)
        count = 0
        for i in range(1):
            for track in tracks: 
                db.execute("INSERT OR IGNORE INTO tracks (name, artist, id) VALUES (?, ?, ?)", track["name"], track["artists"][0]["name"], track["id"])
                count += 1
            albums = get_albums(token, artist)
            for album in albums:
                tracks = get_tracks_from_album(token, album["id"])
                for track in tracks:
                    db.execute("INSERT OR IGNORE INTO tracks (name, artist, id) VALUES (?, ?, ?)", track["name"], track["artists"][0]["name"], track["id"])
                    count +=1 
                    if count >= 20:
                        break
                if count >= 20:
                    break
    if input5 and input5a:
        artist = search_for_artist_id(token, input5a)
        tracks = most_popular_tracks(token, artist)
        count = 0
        for i in range(1):
            for track in tracks: 
                db.execute("INSERT OR IGNORE INTO tracks (name, artist, id) VALUES (?, ?, ?)", track["name"], track["artists"][0]["name"], track["id"])
                count += 1
            albums = get_albums(token, artist)
            for album in albums:
                tracks = get_tracks_from_album(token, album["id"])
                for track in tracks:
                    db.execute("INSERT OR IGNORE INTO tracks (name, artist, id) VALUES (?, ?, ?)", track["name"], track["artists"][0]["name"], track["id"])
                    count +=1 
                    if count >= 20:
                        break
                if count >= 20:
                    break
    songs = db.execute("SELECT * FROM tracks ORDER BY RANDOM() LIMIT 20") 
    return render_template("mode2.html", songs=songs)
@app.route("/mode3")
def mode3():
    db.execute("DELETE FROM tracks")
    # Get inputs from URL parameters
    input1 = request.args.get("input1")
    input1a = request.args.get("input1a")
    input2 = request.args.get("input2") 
    input2a = request.args.get("input2a")
    input3 = request.args.get("input3")
    input3a = request.args.get("input3a")
    input4 = request.args.get("input4")
    input4a = request.args.get("input4a")    
    input5 = request.args.get("input5")
    input5a = request.args.get("input5a")
    

    # Get most popular tracks
    #if input1 and input1a:
    artist1 = search_for_artist_id(token, input1a)
    tracks1 = most_popular_tracks(token, artist1)
    count = 0
    for i in range(1):
        for track in tracks1: 
            db.execute("INSERT OR IGNORE INTO tracks (name, artist, id) VALUES (?, ?, ?)", track["name"], track["artists"][0]["name"], track["id"])
            count += 1
        albums = get_albums(token, artist1)
        for album in albums:
            tracks = get_tracks_from_album(token, album["id"])
            for track in tracks:
                db.execute("INSERT OR IGNORE INTO tracks (name, artist, id) VALUES (?, ?, ?)", track["name"], track["artists"][0]["name"], track["id"])
                count +=1 
                if count >= 10:
                    break
            if count >= 10:
                break
    
    if input2 and input2a:
        artist = search_for_artist_id(token, input2a)
        tracks = most_popular_tracks(token, artist)
        count = 0
        for i in range(1):
            for track in tracks: 
                db.execute("INSERT OR IGNORE INTO tracks (name, artist, id) VALUES (?, ?, ?)", track["name"], track["artists"][0]["name"], track["id"])
                count += 1
            albums = get_albums(token, artist)
            for album in albums:
                tracks = get_tracks_from_album(token, album["id"])
                for track in tracks:
                    db.execute("INSERT OR IGNORE INTO tracks (name, artist, id) VALUES (?, ?, ?)", track["name"], track["artists"][0]["name"], track["id"])
                    count +=1 
                    if count >= 10:
                        break
                if count >= 10:
                    break
    if input3 and input3a:
        artist = search_for_artist_id(token, input3a)
        tracks = most_popular_tracks(token, artist)
        count = 0
        for i in range(1):
            for track in tracks: 
                db.execute("INSERT OR IGNORE INTO tracks (name, artist, id) VALUES (?, ?, ?)", track["name"], track["artists"][0]["name"], track["id"])
                count += 1
            albums = get_albums(token, artist)
            for album in albums:
                tracks = get_tracks_from_album(token, album["id"])
                for track in tracks:
                    db.execute("INSERT OR IGNORE INTO tracks (name, artist, id) VALUES (?, ?, ?)", track["name"], track["artists"][0]["name"], track["id"])
                    count +=1 
                    if count >= 10:
                        break
                if count >= 10:
                    break 
    if input4 and input4a:
        artist = search_for_artist_id(token, input4a)
        tracks = most_popular_tracks(token, artist)
        count = 0
        for i in range(1):
            for track in tracks: 
                db.execute("INSERT OR IGNORE INTO tracks (name, artist, id) VALUES (?, ?, ?)", track["name"], track["artists"][0]["name"], track["id"])
                count += 1
            albums = get_albums(token, artist)
            for album in albums:
                tracks = get_tracks_from_album(token, album["id"])
                for track in tracks:
                    db.execute("INSERT OR IGNORE INTO tracks (name, artist, id) VALUES (?, ?, ?)", track["name"], track["artists"][0]["name"], track["id"])
                    count +=1 
                    if count >= 10:
                        break
                if count >= 10:
                    break
    if input5 and input5a:
        artist = search_for_artist_id(token, input5a)
        tracks = most_popular_tracks(token, artist)
        count = 0
        for i in range(1):
            for track in tracks: 
                db.execute("INSERT OR IGNORE INTO tracks (name, artist, id) VALUES (?, ?, ?)", track["name"], track["artists"][0]["name"], track["id"])
                count += 1
            albums = get_albums(token, artist)
            for album in albums:
                tracks = get_tracks_from_album(token, album["id"])
                for track in tracks:
                    db.execute("INSERT OR IGNORE INTO tracks (name, artist, id) VALUES (?, ?, ?)", track["name"], track["artists"][0]["name"], track["id"])
                    count +=1 
                    if count >= 10:
                        break
                if count >= 10:
                    break
    songs = db.execute("SELECT * FROM tracks ORDER BY RANDOM() LIMIT 10") 
    return render_template("mode3.html", songs=songs)



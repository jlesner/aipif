from flask import Flask, redirect, render_template, request, url_for
from api.FsWebApi import FsWebApi
from flask_cors import CORS

app = Flask(__name__)
# CORS(app)
CORS(app, resources={r"/*": {"origins": "*"}})

web_api = FsWebApi("src/story/_queue")

@app.route("/sl", methods=("GET", "POST"))
def story_list():
    return web_api.json_story_list()


@app.route("/ss", methods=("GET", "POST"))
def story_suggest():

    if request.method == "GET":
        story_suggestion = request.args.get("ss")
        print(f"{story_suggestion} story suggestion" )
        web_api.story_suggest(story_suggestion)

    return redirect("http://aipif-2023.s3.amazonaws.com/static/story_list4.html?m=ty")


@app.route("/prr", methods=("GET", "POST"))
def picture_retry_request():

    if request.method == "GET":
        id = request.args.get("id")
        print(f"retry_request(id) with {id}" )
        web_api.retry_request(id)

    return "request fufilled"

@app.route("/mrr", methods=("GET", "POST"))
def music_retry_request():

    if request.method == "GET":
        id = request.args.get("id")
        print(f"retry_request(id) with {id}" )
        web_api.retry_request(id)

    return "request fufilled"

@app.route("/srr", methods=("GET", "POST"))
def sound_retry_request():

    if request.method == "GET":
        id = request.args.get("id")
        print(f"retry_request(id) with {id}" )
        web_api.retry_request(id)

    return "request fufilled"

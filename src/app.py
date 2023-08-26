from flask import Flask, redirect, render_template, request, url_for
from api.FsWebApi import FsWebApi
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

web_api = FsWebApi("src/story/_queue")

@app.route("/sl", methods=("GET", "POST"))
def story_list():
    return web_api.json_story_list()



@app.route("/ss", methods=("GET", "POST"))
def story_suggest():

    if request.method == "GET":
        story_suggestion = request.args.get("ss")
        web_api.story_suggest(story_suggestion)
        print(f"{story_suggestion} story suggestion" )

    return redirect("https://aipif-2023.s3.amazonaws.com/static/story_list.html?m=ty")



@app.route("/rr", methods=("GET", "POST"))
def story_suggest():

    if request.method == "GET":
        id = request.args.get("id")
        web_api.request_retry(id)
        print(f"request_retry(id) with {id}" )

    return None


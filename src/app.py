from api.S3WebApi import S3WebApi
from flask import Flask, redirect, render_template, request, url_for
from api.FsWebApi import FsWebApi
from flask_cors import CORS

app = Flask(__name__)
# CORS(app)
CORS(app, resources={r"/*": {"origins": "*"}})

# web_api = FsWebApi("src/story/_queue")
web_api = S3WebApi()

@app.route("/sl", methods=("GET", "POST"))
def story_list():
    return web_api.json_story_list()


@app.route("/ss", methods=("GET", "POST"))
def story_suggest():

    if request.method == "GET":
        story_suggestion = request.args.get("ss")
        print(f"story_suggest() with {story_suggestion}" )
        web_api.story_suggest(story_suggestion)

    # return redirect("http://aipif-2023.s3.amazonaws.com/static/story_list4.html?m=ty")
    return "OK"


@app.route("/pr", methods=("GET", "POST"))
def picture_retry():

    if request.method == "GET":
        id = request.args.get("id")
        print(f"picture_retry(id) with {id}" )
        web_api.picture_retry(id)

    return "OK"

@app.route("/mr", methods=("GET", "POST"))
def music_retry():

    if request.method == "GET":
        id = request.args.get("id")
        print(f"music_retry(id) with {id}" )
        web_api.music_retry(id)

    return "OK"

@app.route("/sr", methods=("GET", "POST"))
def sound_retry():

    if request.method == "GET":
        id = request.args.get("id")
        print(f"sound_retry(id) with {id}" )
        web_api.sound_retry(id)

    return "OK"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
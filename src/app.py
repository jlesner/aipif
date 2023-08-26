import os

# import openai
from flask import Flask, redirect, render_template, request, url_for

from api.FsWebApi import FsWebApi

app = Flask(__name__)
web_api = FsWebApi()


@app.route("/ss", methods=("GET", "POST"))
def story_suggest():

    if request.method == "GET":
        story_suggestion = request.args.get("ss")
        web_api.story_suggest(story_suggestion)
        print(f"{story_suggestion} story suggestion" )

    return redirect("https://aipif-2023.s3.amazonaws.com/static/story_list.html?m=ty")


@app.route("/sl", methods=("GET", "POST"))
def story_list():
    return web_api.json_story_list()


# @app.route("/", methods=("GET", "POST"))
# def index():
#     if request.method == "POST":
#         animal = request.form["animal"]
#         response = openai.Completion.create(
#             model="text-davinci-003",
#             prompt=generate_prompt(animal),
#             temperature=0.6,
#         )
#         return redirect(url_for("index", result=response.choices[0].text))

#     result = request.args.get("result")
#     return render_template("index.html", result=result)


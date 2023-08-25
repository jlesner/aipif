import os

import openai
from flask import Flask, redirect, render_template, request, url_for
from story.seeds.image_seeds import *


app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_first_emoji_values(emoji_descriptions):
    first_values = [emoji for emoji, _ in emoji_descriptions]
    result = " ".join(first_values)
    return result

@app.route("/emoji", methods=("GET", "POST"))
def emoji():
    emoji_list = get_first_emoji_values(emoji_descriptions2)

    return render_template("emoji.html", emoji=str(emoji_list))


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        animal = request.form["animal"]
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt(animal),
            temperature=0.6,
        )
        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("index.html", result=result)



@app.route("/story_suggest", methods=("GET", "POST"))
def index():
    # if request.method == "POST":
    #     animal = request.form["animal"]
    #     response = openai.Completion.create(
    #         model="text-davinci-003",
    #         prompt=generate_prompt(animal),
    #         temperature=0.6,
    #     )
    #     # TODO assign story_suggestion from ss URL parameter

    story_suggestion = request.args.get("ss")
                
    print(f"{story_suggestion} story suggestion" )
    # return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("index.html", result=result)



def generate_prompt(animal):
    return """Suggest three names for an animal that is a superhero.

Animal: Cat
Names: Captain Sharpclaw, Agent Fluffball, The Incredible Feline
Animal: Dog
Names: Ruff the Protector, Wonder Canine, Sir Barks-a-Lot
Animal: {}
Names:""".format(
        animal.capitalize()
    )

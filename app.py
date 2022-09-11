import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=("GET",))
def clear():
    return render_template("index.html", result="")

@app.route("/results", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        position = request.form["position"]
        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=generate_prompt(position),
            temperature=0.6,
        )
        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("index.html", result=result)


def generate_prompt(position):
    return """Suggest three top NFL players to draft in fantasy football this season. 
    
Position: RB
Names: Nick Chubb, Jonathan Taylor, Christan McCaffrey
Position: Wide Receiver
Names: Davante Adams, Tyreek Hill, Cooper Kupp
Position: {}
Names:""".format(
        position.capitalize()
    )

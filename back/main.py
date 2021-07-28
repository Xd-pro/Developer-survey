from scarletdb import ScarletDB
from flask import Flask, request, jsonify, render_template, Response
import random
from replit import db as rdb
from replit.web import auth, sign_in_snippet
import os

def redirect(url):
  resp = Response(f"""<head><meta http-equiv="Refresh" content="0; url='{url}'" /></head>Redirecting! If it doesn't work, click this link: {url}""", status=304, headers={
    "Location": url
  })
  return resp

app = Flask(__name__, static_url_path="", static_folder="../front/dist", template_folder="../front/dist")
app.secret_key = os.environ["SECRET"]

QUESTION = "What's your favourite server-side web programming language?"
OPTIONS = ["Python", "Ruby", "Node.js", "C#", "Scala", "Go", "PHP", "Perl"]

answers = ScarletDB([])
answers.replit("answers")

QUESTION_INDEX = 2

if "prev_index" not in rdb.keys():
  rdb["prev_index"] = 0

if not rdb["prev_index"] == QUESTION_INDEX:
  print("Clearing")
  answers.clear()

rdb["prev_index"] = QUESTION_INDEX

@app.after_request
def after_request(res):
  res.headers["Access-Control-Allow-Origin"] = "*"
  return res

@app.route("/")
def index():
  return render_template("index.html")

@app.errorhandler(404)
def handle_404(e):
  return render_template("index.html")

@app.route("/login")
def login():
  if not auth.user_id:
    return f"""<html><body>{sign_in_snippet}</body></html>"""
  else:
    rdir = request.args.get("next", "/NotFound")
    if not rdir.startswith("https://Developer-survey.xfinnbar.repl.co") or count_char(rdir, "/") == 1:
      return redirect(rdir), 200

def count_char(in_str, in_char):
  count = 0
  for char in in_str:
    if char == in_char:
      count += 1


@app.route("/api/answer")
def answer():
  if not auth.user_id:
    return "Not logged in!", 403
  id = auth.user_id
  if len(answers.get({"id": id})) == 0:
    if request.args.get("choice") not in OPTIONS:
      return "Invalid language!", 400
    answers.insert({
      "id": id,
      "choice": request.args.get("choice")
    })
    return redirect("/results")
  else:
    return redirect("/already_sumbitted"), 400

@app.route("/api/has_answered")
def has_answered():
  return jsonify({"has_answered": len(answers.get({"id": auth.user_id})) != 0})

@app.route("/api/get_answers")
def get_anwsers():
  retval = {}
  for i in answers.list:
    if i["choice"] not in retval.keys():
      retval[i["choice"]] = 0
    if "total" not in retval.keys():
      retval["total"] = 0
    retval[i["choice"]] += 1
    retval["total"] += 1
  return jsonify(retval)

@app.route("/api/get_choices")
def get_choices():
  return jsonify({"options": OPTIONS, "question": QUESTION, "has_answered": len(answers.get({"id": auth.user_id})) != 0})

app.run("0.0.0.0")
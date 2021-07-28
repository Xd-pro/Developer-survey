from scarletdb import ScarletDB
from flask import Flask, request, session, jsonify
import random
from replit import db as rdb
import os

app = Flask(__name__)
app.secret_key = os.environ["SECRET"]

QUESTION = "What's your favourite server-side web programming language?"
OPTIONS = ["Python", "Ruby", "Node.js", "C#", "Scala", "Go", "PHP", "Perl"]

answers = ScarletDB([])
answers.replit("answers")

QUESTION_INDEX = 2

if "prev_index" not in rdb.keys():
  rdb["prev_index"] = 0

if not rdb["prev_index"] == QUESTION_INDEX:
  answers.clear()

rdb["prev_index"] = QUESTION_INDEX

@app.after_request
def after_request(res):
  res.headers["Access-Control-Allow-Origin"] = "*"
  return res

def assign_id():
  i = random.randint(100000, 9999999)
  if "ids" not in rdb.keys():
    rdb["ids"] = []
  while i in rdb["ids"]:
    i = random.randint(100000, 9999999)
  rdb["ids"].append(i)
  return i

@app.route("/api/answer")
def answer():
  if "id" not in session.keys():
    id = assign_id()
    session["id"] = id
  else:
    id = session["id"]
  if len(answers.get({"id": id})) == 0:
    if request.args.get("choice") not in OPTIONS:
      return "Invalid language!", 400
    answers.insert({
      "id": id,
      "choice": request.args.get("choice")
    })
    return "Answer submitted!", 200
  else:
    return "Already answered!", 400

@app.route("/api/has_answered")
def has_answered():
  return jsonify({"has_answered": len(answers.get({"id": session.get("id", None)})) != 0})

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
  return jsonify({"options": OPTIONS, "question": QUESTION, "has_answered": len(answers.get({"id": session.get("id", None)})) != 0})

app.run("0.0.0.0")
import os
import json
import random
import re

import openai
from flask import Flask, request, session, send_from_directory

from database import Database, Highscore

app = Flask(__name__)
app.secret_key = os.urandom(64)
openai.organization = os.environ['OPENAI_API_ORG_ID']
openai.api_key = os.environ['OPENAI_API_KEY']

with open('./topics.json') as f:
    TOPICS = json.load(f)
with open('./questions.json') as f:
    QUESTIONS = json.load(f)
NUM_TRIES = 5


def get_candidate_questions():
    answered_questions = session['question_answered']
    all_questions = range(len(QUESTIONS['questions']))
    available_questions = set(all_questions) - set(answered_questions)

    size = min(4, len(available_questions))
    candidate_questions = random.sample(available_questions, size)
    session["candidate_questions"] = candidate_questions
    return [QUESTIONS['questions'][idx] for idx in candidate_questions]


def evaluate_answer(data):
    topic = session['topic']
    answer = TOPICS['topics'][topic]

    reward = 0
    correct_answers = 0
    total_answers = 0

    reason = "Incorrect guess"
    for key in data.keys():
        if key == 'name':
            total_answers += 1
            for accepted_name in answer['names']:
                if accepted_name.lower().replace(' ','') == data['name'].lower().replace(' ',''):
                    reason = "Name correct"
                    correct_answers += 1
                    reward += 225
                    break
        elif key == 'country':
            total_answers += 1
            for accepted_place in answer['countries']:
                if accepted_place.lower().replace(' ','') == data['country'].lower().replace(' ',''):
                    reason = "Civilization correct"
                    correct_answers += 1
                    reward += 50
                    break
        elif key == 'century':
            total_answers += 1
            if answer['century'] == data['century']:
                correct_answers += 1
                reason = "Century correct"
                reward += 75

    # negative 10 points for wrong guesses
    reward += (-10 * (total_answers - correct_answers))


    session['score'] += reward

    return False, session['score'], reward, reason


def prepare_prompt(question_selected):
    question_str = QUESTIONS['questions'][question_selected]
    topic = session['topic']
    name = TOPICS['topics'][topic]['names'][0]
    prompt = f"""The following is a conversation with {name}.

{name}: My name is {name}.  What questions can I answer for you?

Human: {name}, {question_str}
{name}:"""
    print('PROMPT:\n',prompt)
    return prompt


def ask_gpt3(prompt, params=None):
    if not params:
        params = {
            "engine": "davinci",
            "temperature": 0.27,
            "stop": ["\n", "."],
        }
    completion = openai.Completion.create(**{"prompt": prompt}, **params)
    response = completion.choices[0].text.replace('\nA:', '')
    topic = session['topic']
    name = TOPICS['topics'][topic]['names'][0]
    response = re.sub(name, '<my name>', response, flags=re.IGNORECASE)
    return response


@app.before_first_request
def initialize_database():
    Database.initialize()


@app.route('/api/start/conversation', methods=['POST', 'GET'])
def start_conversation():
    session.clear()

    data = request.get_json()
    username = data['username']

    session['username'] = username
    session['topic'] = random.randrange(0, len(TOPICS['topics']))
    print('PICKING', session['topic'])
    session['score'] = 0
    session['question_answered'] = []
    session['remaining_tries'] = NUM_TRIES

    candidate_questions = get_candidate_questions()
    d = {
        "questions": candidate_questions,
        # Putting the "initial" censored response
        "response": "My name is ___________.  What questions can I answer for you?",
        "questions_answered": session['question_answered']
    }
    return json.dumps(d)


@app.route('/api/ask/question', methods=['POST', 'GET'])
def ask_question():
    data = request.get_json()
    question_selected = session['candidate_questions'][data['question']]
    prompt = prepare_prompt(question_selected)
    gpt3_response = ask_gpt3(prompt)
    print('>>', gpt3_response)
    session['question_answered'].append(question_selected)
    candidate_questions = get_candidate_questions()
    d = {
        "response": gpt3_response,
        # next round of questions
        "questions": candidate_questions,
        # "candidate_questions": session['candidate_questions'],
        # "question_answered": session['question_answered'],
        # "prompt": prompt,
    }
    return json.dumps(d)


@app.route('/api/submit/answer', methods=['POST', 'GET'])
def submit_answer():
    data = request.get_json()
    correct, score, reward, reason = evaluate_answer(data)
    if correct:
        session['remaining_tries'] = 0
    else:
        session['remaining_tries'] -= 1
    d = {
        "correct": correct,
        "remaining-tries": session['remaining_tries'],
        "score": score,
        "reward": reward,
        "reason": reason
    }
    return json.dumps(d)


@app.route('/api/finish', methods=['GET'])
def finish():
    topic = session['topic']
    answer = TOPICS['topics'][topic]
    highscore = Highscore(session['username'], session['score'], answer['names'][0])
    highscore.save_to_mongo()
    session.clear()
    return json.dumps(answer)

def send_1():
    return send_from_directory('../history-guesser/dist/', 'index.html')

@app.route('/')
@app.route('/about')
@app.route('/contact')
@app.route('/highscores')
def send_1():
    return send_from_directory('../history-guesser/dist/', 'index.html')

@app.route('/<path:path>')
def send_rest(path):
    return send_from_directory('../history-guesser/dist/', path)


@app.route('/api/highscore', methods=['GET'])
def high_score():
    highscores = Database.find_top_n('highscores', 'score', 100)
    d = {"scores": highscores}
    return json.dumps(d)



if __name__ == '__main__':
    # set FLASK_ENV=development  to enable debug (safer)
    app.run(port=5000)

from flask import Flask, request, session
import os
import json
import random
import openai
import re


app = Flask(__name__)
app.secret_key = os.urandom(64)
openai.organization = os.environ['OPENAI_API_ORG_ID']
openai.api_key = os.environ['OPENAI_API_KEY']

with open('./topics.json') as f:
    TOPICS = json.load(f)
with open('./questions.json') as f:
    QUESTIONS = json.load(f)
NUM_TRIES = 5
PENALTY = {'name': 30, 'country': 20, 'century': 10}
REWARD = {'name': 100, 'country': 80, 'century': 50}


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

    assert len(data) == 1
    k, v = list(*data.items())

    if answer[k].lower() == str(v).lower():
        session['score'] += REWARD[k]
        return True, session['score'], REWARD[k]
    session['score'] -= PENALTY[k]
    return False, session['score'], -PENALTY[k]


def prepare_prompt(question_selected):
    question_str = QUESTIONS['questions'][question_selected]
    topic = session['topic']
    name = TOPICS['topics'][topic]['name']
    prompt = "I am a friendly and intelligent chatbot. If you ask me a question about me that is rooted in truth, " \
             "I will give you the answer. If you ask me a question that is nonsense, trickery, or has no clear " \
             "answer, I will respond with 'Unknown'. " \
             f"\nQ:{name}, {question_str}"
    return prompt


def ask_gpt3(prompt, params=None):
    if not params:
        params = {
            "engine": "davinci",
            "temperature": 0.07,
            "stop": ["\xa0Q: ", "."],
        }
    completion = openai.Completion.create(**{"prompt": prompt}, **params)
    print(completion)
    response = completion.choices[0].text.replace('\nA: ', '')
    topic = session['topic']
    name = TOPICS['topics'][topic]['name']
    response = re.sub(name, '<my name>', response, flags=re.IGNORECASE)
    return response


@app.route('/start/conversation', methods=['POST', 'GET'])
def start_conversation():
    session.clear()

    data = request.get_json()
    username = data['username']

    session['username'] = username
    session['topic'] = random.randrange(len(TOPICS))
    session['score'] = 100
    session['question_answered'] = []
    session['remaining_tries'] = NUM_TRIES

    candidate_questions = get_candidate_questions()
    d = {
        "questions": candidate_questions,
        "hint": "blah",
        "questions_answered": session['question_answered']
    }
    return json.dumps(d)


@app.route('/ask/question', methods=['POST', 'GET'])
def ask_question():
    data = request.get_json()
    question_selected = session['candidate_questions'][data['question']]
    prompt = prepare_prompt(question_selected)
    gpt3_response = ask_gpt3(prompt)
    print(prompt)
    print(gpt3_response)
    session['question_answered'].append(question_selected)
    candidate_questions = get_candidate_questions()
    d = {
        "response": gpt3_response,
        # next round of questions
        "questions": candidate_questions,
        # "candidate_questions": session['candidate_questions'],
        "question_answered": session['question_answered'],
        "prompt": prompt
    }
    return json.dumps(d)


@app.route('/submit/answer', methods=['POST', 'GET'])
def submit_answer():
    data = request.get_json()
    correct, score, reward = evaluate_answer(data)
    if correct:
        session['remaining_tries'] = 0
    else:
        session['remaining_tries'] -= 1
    d = {
        "correct": correct,
        "remaining-tries": session['remaining_tries'],
        "score": score,
        "reward": reward
    }
    return json.dumps(d)


@app.route('/finish', methods=['GET'])
def finish():
    topic = session['topic']
    answer = TOPICS['topics'][topic]
    return json.dumps(answer)


if __name__ == '__main__':
    app.run(debug=True, port=5000)

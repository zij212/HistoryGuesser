from flask import Flask, request, session
import json
import random

app = Flask(__name__)
# TODO move secret key out
app.secret_key = 'x1q5VK$**haH45aVgbsm#NIJUs6tU0Hj4HG*0duMMGB2'

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


@app.route('/start/conversation', methods=['POST', 'GET'])
def start_conversation():
    session.clear()
    data = request.get_json()
    username = data['username']
    # TODO choose a topic
    session['topic'] = 1

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
    question_asked = session['candidate_questions'][data['question']]
    # TODO ask gpt-3 to answer <QUESTIONS['questions'][question_asked]> in context of <session['topic']>
    gpt3_response = "A" + QUESTIONS['questions'][question_asked]
    session['question_answered'].append(question_asked)
    candidate_questions = get_candidate_questions()
    d = {
        "response": gpt3_response,
        # next round of questions
        "questions": candidate_questions,
        # "candidate_questions": session['candidate_questions'],
        "question_answered": session['question_answered']
    }
    return json.dumps(d)


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

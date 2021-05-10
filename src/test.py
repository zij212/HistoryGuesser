import sys, random
from app import prepare_prompt, ask_gpt3, TOPICS, QUESTIONS



import sys
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('usage: %s <number of topics to test> <question in quotes>')
    
    count = int(sys.argv[1])
    question = sys.argv[2]

    for i in range(0, count):
        rand = random.randrange(0, len(TOPICS['topics']))
        topic = TOPICS['topics'][rand]

        prompt = prepare_prompt(question, topic)
        gpt3_response = ask_gpt3(prompt, topic)

        print(f"{topic['names'][0]}:", gpt3_response)

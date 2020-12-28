import nltk
import json
import os
from preprocessing import preprocess

file_name = "squad_dev.json"
out_file_name = 'squad_dev_out'

# Q and A filtering is done below, explained in writeup.
Q_A_pairs = []
Q = []
A = []

with open(file_name) as json_file:
    data = json.load(json_file)['data']

MAX_LENGTH = 20 # Maximum sentence length to consider

for topic in data:
    for paragraph in topic['paragraphs']:
        for qas in paragraph['qas']:
            if qas['is_impossible']:
                continue
            question = preprocess(qas['question'])
            answer = preprocess(qas['answers'][0]['text'])
            words_in_question = len(question.split(' '))
            words_in_answer = len(answer.split(' '))
            if 0 < words_in_question < MAX_LENGTH and 0 < words_in_answer < MAX_LENGTH \
                    and question != "" and answer != "":
                Q_A_pairs.append((question, answer))
                Q.append(question)
                A.append(answer)



dump = {
    "signature": f"{file_name} (last_mod: {os.path.getmtime(file_name)})",
    "data": Q_A_pairs,
    "questions": Q,
    "answers": A
}

with open(f"{out_file_name}.json", 'w', encoding='utf-8') as f:
    json.dump(dump, f)
print(f"\nDone. Wrote json file as: '{out_file_name}.json'")

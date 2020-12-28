import json
import os
from preprocessing import preprocess

file_name = "multi_woz.json"
out_file_name = 'multi_woz_out'

# Q and A filtering is done below, explained in writeup.
Q_A_pairs = []
Q = []
A = []

with open(file_name) as json_file:
    data = json.load(json_file)

MAX_LENGTH = 20 # Maximum sentence length to consider

question = ""
for convo in data.items():
    for num, log in enumerate(convo[1]['log'], start=1):
        processed = preprocess(log['text'])
        if (num % 2) != 0:
            question = processed
        else:
            answer = processed
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

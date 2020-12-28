import json
import os
from preprocessing import preprocess

dat = []

file_name = "frasier_transcripts.csv"
out_file_name = 'frasier_dialog_out'

data = open(file_name, encoding='utf-8', errors='ignore').read().split('\n')

if not data[-1]:
    data.pop()

data = data[2:]

# Q and A filtering is done below, explained in writeup.
Q_A_pairs = []
Q = []
A = []

file = open(file_name, "r").read().split("\n")

MAX_LENGTH = 20 # Maximum sentence length to consider

last_line = ()
for i in range(len(data) - 1):
    character, dialog, season, episode = data[i][1:].split('","')[:4]
    processed = preprocess(dialog)
    if dialog == '':
        continue
    if character != 'Frasier':
        last_line = (i, dialog, episode)
        continue
    if i == 0:
        continue
    if i == (last_line[0]+1) and episode == last_line[2] and character == 'Frasier':
        answer = processed
        question = last_line[1]
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

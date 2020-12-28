from .preprocessing import preprocess
import re

out_file_name = 'suggested_Q&A.txt'

incorrect_identifiers = [
    "that is wrong i expected",
    "that is wrong you should have said",
    "incorrect i expected",
    "incorrect you should have said ",
]

def incorrectAnswer(text):
    processed_text = preprocess(text)
    for id in incorrect_identifiers:
        if id in processed_text:
            return True

def saveQuestionAnswerPairs(question, answer):
    processed_question = preprocess(question)
    processed_answer = preprocess(answer)

    for id in incorrect_identifiers:
        processed_answer = re.sub(id, r"", processed_answer).strip()

    if processed_answer is not "" and processed_question is not "":
        file = open(out_file_name, "a+")
        file.write(processed_question + "\n")
        file.write(processed_answer + "\n")
        file.close()
import spacy
import sys
from .preprocessing import preprocess
import re

nlp = spacy.load("en_core_web_lg")

user_questions = [
    ("name", ["whats my name", "what is my name", "what am i called", "who am i", "do you know my name"]),
    ("age", ['how old am i', 'what is my age', 'whats my age', 'do you know my age']),
    ("location", ['where am i', 'where do i live', 'what is my location', 'where am i from'])
]

questions = [
    ("What is your name?", "PERSON", "name"),
    ("What is your age?", "CARDINAL", "age"),
    ("Where do you live?", "GPE", "location")
]
state = {
  "name": "",
  "age": "",
  "location": ""
}

def askQuestions():
    count = 0
    while True:
        if count > (len(questions)):
            print("Thank you. How can I help you?")
            return True

        if count == 0:
            print("Can I ask you some questions about yourself? (y/n)")
            sys.stdout.write(">")
            sys.stdout.flush()
            input_str = input()
            if input_str[0:1].lower() != 'y':
                print("Ok. How can I help you?")
                return True

        if count > 0:
            print(questions[count-1][0])
            sys.stdout.write(">")
            sys.stdout.flush()
            input_str = input()
            entity = getEntity(input_str, questions[count - 1][1])
            if not entity:
                print("Sorry, I didn't understand your answer. Could you please try again.")
                count -= 1
            else:
                state.update({questions[count - 1][2]: entity.text})
            print("")

        count += 1

def getEntity(input_str, label):
    for ent in nlp(input_str).ents:
        if ent.label_ == label:
            return ent
    return None

def getAnswer(text):
    if '?' not in text:
        return ""
    text = re.sub(r"\?+", r"", text)
    processed_text = preprocess(text)
    for question in user_questions:
        for version in question[1]:
            if version in processed_text:
                if state[question[0]] == "":
                    return "Sorry. I don't know your " + question[0]
                return state[question[0]]
    return ""
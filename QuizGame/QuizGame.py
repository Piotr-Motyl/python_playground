import html
import requests

class Question:
    def __init__(self, category, question_str, correct_answer_flag):
        self.category = category
        self.question_str = question_str
        self.correct_answer_flag = correct_answer_flag

class Quiz:
    def __init__(self, question_number):
        self.api_url = "https://opentdb.com/api.php?difficulty=easy&type=boolean&amount="
        self.question_number = question_number
        self.questions_list = []
        self.load_questions(question_number)

    def load_questions(self, question_number):
        response = requests.get(self.api_url + str(question_number))
        if response.ok:
            data = response.json()
            result = data["results"]

            for question in result:
                category = question["category"]
                question_str = html.unescape(question["question"])
                correct_answer_flag = question["correct_answer"].lower() in ['true', 1, 'yes']

                question_obj = Question(category, question_str, correct_answer_flag)
                self.questions_list.append(question_obj)

    def start_quiz(self):
        print("*** ||| START QUIZ ||| ***")
        correct_user_answer_num = 0
        n = 0
        questions_number = len(self.questions_list)

        while n < questions_number:
            q = self.questions_list[n]
            print("??? Question number " + str(n) + "/"
                  + str(user_questions_quantity)
                  + ": ???\n", q.question_str)
            answer = input("=== Give answer: yes(y)/no(n) --->")
            answer_bool = False
            if answer.lower() == "y":
                answer_bool = True
            if answer_bool == q.correct_answer_flag:
                print("*** CORRECT! ***\n")
                correct_user_answer_num += 1
            else:
                print("*** NOT CORRECT! ***\n")
            n += 1

        print("*** Number correct answers: (", correct_user_answer_num, ") from (", len(self.questions_list), ") questions ***")

while True:
    user_questions_quantity = input("=== Select number of questions in Quiz Game or exit(e) ===\n")

    if user_questions_quantity.lower() == "e" or user_questions_quantity.lower() == "exit":
        print("*** END ***")
        break

    try:
        user_questions_quantity = int(user_questions_quantity)
        quiz = Quiz(user_questions_quantity)
        quiz.start_quiz()
        break
    except ValueError:
        print("=== Selected char is not a number, please select again ===\n")
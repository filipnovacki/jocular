import jsonpickle
# from cloze.questions import ClozeQuestion
from cloze.templates import fill_numerical
from pprint import pprint
from cloze.cloze_question import ClozeQuestion, ClozeResponse, ClozeAnswer, Numerical

q = ClozeQuestion("Koliko je {} + {}?")
q.fill_question_parameters(5, 3)
print(q)

r = Numerical(10)
for x in range(5):
    ponder = 0
    feedback = "Wrong"
    is_correct = False
    if x == 3:
        ponder = 1
        feedback = "Correct"
        is_correct = True
    ans = ClozeAnswer(answer_text=str(x+4), ponder=ponder, feedback=feedback, is_correct=is_correct)
    r.add_possible_answer(ans)

q.add_response(r)
q.export()

print(q.export_cloze_question())


# q = ClozeQuestion("pfdisa {2:NM:~%100%17:0} dsaf")

# q_pickle = jsonpickle.dumps(q)
# print(q_pickle)

# print(q.solve([7]))

# print(Question("""
# This question consists of some text with an answer embedded right here
# {1:MULTICHOICE:Wrong answer#Feedback for this wrong answer~Another wrong answer#Feedback for the other wrong answer~=Correct answer#Feedback for correct answer~%50%Answer that gives half the credit#Feedback for half credit answer} and right after that you will have to deal with this short answer
# {1:SHORTANSWER:Wrong answer#Feedback for this wrong answer~=Correct answer#Feedback for correct answer~%50%Answer that gives half the credit#Feedback for half credit answer} and finally we have a floating point number
# {2:NUMERICAL:=23.8:0.1#Feedback for correct answer 23.8~%50%23.8:2#Feedback for half credit answer in the nearby region of the correct answer}. The multichoice question can also be shown in the vertical display of the standard moodle multiple choice.
# {2:MCV:1. Wrong answer#Feedback for this wrong answer~2. Another wrong answer#Feedback for the other wrong answer~=3. Correct answer#Feedback for correct answer~%50%4. Answer that gives half the credit#Feedback for half credit answer} Or in an horizontal display that is included here in a table
# {2:MCH:a. Wrong answer#Feedback for this wrong answer~b. Another wrong answer#Feedback for the other wrong answer~=c. Correct answer#Feedback for correct answer~%50%d. Answer that gives half the credit#Feedback for half credit answer} A shortanswer question where case must match. Write moodle in upper case letters
# {1:SHORTANSWER_C:moodle#Feedback for moodle in lower case ~=MOODLE#Feedback for MOODLE in upper case ~%50%Moodle#Feedback for only first letter in upper case} Note that addresses like www.moodle.org and smileys :-) all work as normal: a) How good is this?
# {:MULTICHOICE:=Yes#Correct~No#We have a different opinion} b) What grade would you give it?
# {3:NUMERICAL:=3:2}
# """))

# print(numerical_response_template.render(weight="bla", question_type="NUMERICAL"))
# print(fill_numerical(points=3, answers=[
#     {"point_ponder": 1, "value": 2, "tolerance": 3, "comment": 'dsajfads'},
#     {"point_ponder": 0.53, "value": 1, "tolerance": 0.01, "comment": 'Komentar'},
# ]))

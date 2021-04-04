import re

_question_types = {
    "SA": ["SA", "MW", "SHORTANSWER"],  # case is unimportant
    "SAC": ["SAC", "MWC", "SHORTANSWER_C"],  # case must match,
    "NM": ["NM", "NUMERICAL"],  #
    "MC": ["MC", "MULTICHOICE"],  # represented as a dropdown menu in-line in the text
    "MCV": ["MCV", "MULTICHOICE_V"],  # multichoice with vertical column radio buttons
    "MCH": ["MCH", "MULTICHOICE_H"],  # represented as a horizontal row of radio-buttons
    "MR": ["MR", "MULTIRESPONSE"],  # represented as a vertical row of checkboxes
    "MRH": ["MRH", "MULTIRESPONSE_H"],  # represented as a horizontal row of checkboxes
}


def find_answer_type(string: str):
    """
    Find which type of question it is based on question
    :param string: question
    :return: instance of adequate Solution inherited class
    """
    for t in _question_types:
        if string.split(":")[1] in _question_types[t]:
            return _class_question_map[t](string)


class Question:
    """
    Contains whole text of a problem
    """
    def __init__(self, text):
        """
        Initialises question from string
        :param text: string of whole problem
        """
        self.original = text
        self.solution_holders = []
        self.question = "Blank question"
        self.parse(text)

    def parse(self, input_string: str):
        """
        Separates solutions from text and stores it in class instance
        :param input_string: string of whole problem
        :return:
        """
        regex = re.compile("{(.*?)}")
        # list of answers contains all
        solutions = regex.findall(input_string)
        for ans in solutions:
            # remove all solutions from question input
            input_string = input_string.replace(ans, "")
            # add specific Solution to solution_holder, ie creates list of Solutions
            self.solution_holders.append(
                find_answer_type(ans)
            )
        # store question that can be displayed
        self.question = input_string

    def solve(self, solution):
        """
        Takes solution and returns score for that answer
        :param solution: answer in any data type that is appropriate
        :return: score
        """

    def __str__(self):
        return "Question: " + self.question + \
               "Solution:\n" + str(self.solution_holders)

    def __repr__(self):
        return self.__str__()


class Answer:
    def __init__(self, points_ponder, value, comment=None):
        self.comment = comment
        self.value = value
        self.points_ponder = points_ponder

    def __repr__(self):
        return "\n\t\tAnswer {}, weights {}/100 points".format(self.value, self.points_ponder) + ", comment is {};".format(self.comment) if self.comment else ";"

    def __str__(self):
        return self.__repr__()


class Solution:
    def __init__(self, text):
        self.original = text
        self.points = None
        self.answers = []
        self.parse(text)

    def parse(self, text):
        """
        Accepts whole string that comes between {} on cloze questions
        :param text: solution string (between {})
        :return:
        """
        params = text.split(":")
        try:
            # try getting points
            self.points = int(params[0])
        except Exception as e:
            # if no points, assume points are 0
            if params[0] == '':
                self.points = 0
        self.separate_possible_answers(params[2:])

    def separate_possible_answers(self, text: str):
        """
        =Yes#Correct~No#We have a different opinion

        moodle#Feedback for moodle in lower case
            ~=MOODLE#Feedback for MOODLE in upper case
            ~%50%Moodle#Feedback for only first letter in upper case
        :param text:
        :return:
        """
        # join in case there are ":" values in answers and then split by ~
        text_list = "".join(text).split("~")
        # find point ponder %100%, %30%, %0%...
        regex_point_ponder = re.compile("%(.*?)%")
        for ans in text_list:
            point_ponder, comment = None, None
            # TODO remove HTML characters
            try:
                # find point ponder
                point_ponder = regex_point_ponder.match(ans).group()
                # remove point ponder from solution
                ans = ans.replace(point_ponder, "")
                # remove % from ponder and turn it to int
                point_ponder = int(point_ponder[1:-1])
            except:
                if ans[0] == "=":
                    # = doesn't work with shortanswer and it is synonimous with %100%
                    point_ponder = 100
                    # remove ponder from ans
                    ans = ans[1:]
                else:
                    print("I failed when looking for point ponder and ans for question '{}'".format(self.original))
            try:
                comment = ans[ans.index("#") + 1:]
                # remove comment from ans
                ans = ans.replace("#" + comment, "")
            except:
                pass
            self.answers.append(Answer(
                value=ans,
                points_ponder=point_ponder,
                comment=comment,
            ))

    def __str__(self):
        return "\n\nAnswer {}: ".format(self.__class__.__name__) + \
               "\n\tPoints: " + str(self.points) + \
               "\n\tSolution: " + str(self.answers)

    def __repr__(self):
        return self.__str__()


class ShortSolution(Solution):
    # TODO: solve * as a wildcard for all incorrect answers
    pass


class ShortSolutionC(ShortSolution):
    pass


class Numerical(Solution):
    pass


class Multichoice(Solution):
    pass


class Multiresponse(Solution):
    pass


_class_question_map = {
    "SA": ShortSolution,
    "SAC": ShortSolutionC,
    "NM": Numerical,
    "MC": Multichoice,
    "MCV": Multichoice,
    "MCH": Multichoice,
    "MR": Multiresponse,
    "MRH": Multiresponse,
}

print(Question("""
This question consists of some text with an answer embedded right here 
{1:MULTICHOICE:Wrong answer#Feedback for this wrong answer~Another wrong answer#Feedback for the other wrong answer~=Correct answer#Feedback for correct answer~%50%Answer that gives half the credit#Feedback for half credit answer} and right after that you will have to deal with this short answer 
{1:SHORTANSWER:Wrong answer#Feedback for this wrong answer~=Correct answer#Feedback for correct answer~%50%Answer that gives half the credit#Feedback for half credit answer} and finally we have a floating point number 
{2:NUMERICAL:=23.8:0.1#Feedback for correct answer 23.8~%50%23.8:2#Feedback for half credit answer in the nearby region of the correct answer}. The multichoice question can also be shown in the vertical display of the standard moodle multiple choice. 
{2:MCV:1. Wrong answer#Feedback for this wrong answer~2. Another wrong answer#Feedback for the other wrong answer~=3. Correct answer#Feedback for correct answer~%50%4. Answer that gives half the credit#Feedback for half credit answer} Or in an horizontal display that is included here in a table 
{2:MCH:a. Wrong answer#Feedback for this wrong answer~b. Another wrong answer#Feedback for the other wrong answer~=c. Correct answer#Feedback for correct answer~%50%d. Answer that gives half the credit#Feedback for half credit answer} A shortanswer question where case must match. Write moodle in upper case letters 
{1:SHORTANSWER_C:moodle#Feedback for moodle in lower case ~=MOODLE#Feedback for MOODLE in upper case ~%50%Moodle#Feedback for only first letter in upper case} Note that addresses like www.moodle.org and smileys :-) all work as normal: a) How good is this? 
{:MULTICHOICE:=Yes#Correct~No#We have a different opinion} b) What grade would you give it? 
{3:NUMERICAL:=3:2}
"""))
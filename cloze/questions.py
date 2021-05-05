import re
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Answer:
    value: str
    comment: str = field(default=None)
    points_ponder: Any = field(default=1.0)
    tolerance: float = field(default=0)

    def __post_init__(self):
        if type(self.points_ponder) == int and 0 <= self.points_ponder <= 1:
            self.points_ponder = float(self.points_ponder)
        elif type(self.points_ponder) == int and not 0 <= self.points_ponder <= 1:
            raise ValueError("Points ponder must be a value between 0 and 1")
        elif type(self.points_ponder) not in (int, float):
            raise TypeError("Points ponder must be a float")


@dataclass
class Response:
    original: str
    answers: list[Answer] = field(default=None)
    points: int = field(default=None)

    def __post_init__(self):
        self.parse()

    def parse(self):
        """
        Accepts whole string that comes between {} on cloze questions
        :param text: solution string (between {})
        :return:
        """
        params = self.original.split(":")
        try:
            # try getting points
            self.points = int(params[0])
        except Exception as e:
            # if no points, assume points are 0
            if params[0] == '':
                self.points = 0
        self.answers = self.separate_possible_answers(params[2:])

    def separate_possible_answers(self, text: str):
        """
        :param text:
        :return:
        """
        # join in case there are ":" values in answers and then split by ~
        text_list = ":".join(text).split("~")
        # find point ponder %100%, %30%, %0%...
        regex_point_ponder = re.compile("%(.*?)%")
        answers = []
        for ans in text_list:
            # avoid blank answers if answer starts with '~'
            if len(ans) == 0:
                continue
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
                if len(ans) != 0 and ans[0] == "=":
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
                comment = None
            ans = ans.split(":")
            value = ans[0]
            try:
                tolerance = ans[1]
            except:
                tolerance = 0
            answers.append(Answer(points_ponder=point_ponder/100, value=value, comment=comment, tolerance=tolerance))
        return answers

    def solve(self, solution):
        raise NotImplementedError


@dataclass
class ClozeQuestion:
    original: str
    solution_holders: list[Response] = field(default_factory=list)
    question: str = field(default="Blank question")

    def __post_init__(self):
        self.solution_holders = self.parse()

    def parse(self):
        """
        Separates solutions from text and stores it in class instance
        :return:
        """
        input_string = self.original
        regex = re.compile("{(.*?)}")
        # list of answers contains all
        solutions = regex.findall(input_string)
        solution_holders = []
        for ans in solutions:
            # remove all solutions from question input
            input_string = input_string.replace(ans, "")
            # add specific Solution to solution_holder, ie creates list of Solutions
            solution_holders.append(
                find_answer_type(ans)
            )
        # store question that can be displayed
        self.question = input_string
        return solution_holders

    def solve(self, solution: list):
        """
        Takes solution and returns score for that answer
        :param solution: answer in any data type that is appropriate
        :return: score
        """
        if len(solution) != len(self.solution_holders):
            raise Exception("Must provide solutions for all questions")

        points = 0
        for ans, q in zip(solution, self.solution_holders):
            points += q.solve(ans)
        return points


class ShortResponse(Response):
    # TODO: solve * as a wildcard for all incorrect answers
    pass


class ShortResponseC(ShortResponse):
    pass


class NumericalResponse(Response):
    def solve(self, solution):
        found_solution = False
        for sol in self.answers:
            # if correct answer is found
            if sol.value != "*" and float(sol.value) - float(sol.tolerance) <= solution <= float(sol.value) + float(
                    sol.tolerance):
                return sol.points_ponder * self.points
        # if correct answer is not found and * has it's own point ponder
        if not found_solution and "*" in [x.value for x in self.answers]:
            return sol.points_ponder * self.points
        return 0


class MultichoiceResponse(Response):
    pass


class Multiresponse(Response):
    pass


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


_class_question_map = {
    "SA": ShortResponse,
    "SAC": ShortResponseC,
    "NM": NumericalResponse,
    "MC": MultichoiceResponse,
    "MCV": MultichoiceResponse,
    "MCH": MultichoiceResponse,
    "MR": Multiresponse,
    "MRH": Multiresponse,
}

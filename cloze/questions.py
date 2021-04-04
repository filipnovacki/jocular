import re


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

    def __str__(self):
        return "Question: " + self.question + \
               "Solution:\n" + str(self.solution_holders)

    def __repr__(self):
        return self.__str__()


class Answer:
    def __init__(self, points_ponder, value, comment=None, tolerance=0):
        self.comment = comment
        self.value = value
        self.points_ponder = points_ponder / 100
        self.tolerance = tolerance

    def __repr__(self):
        return "\n\t\tAnswer {}, weights {}/100 points, comment {}, tolerance {}" \
            .format(self.value, self.points_ponder, self.comment, self.tolerance)

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
        :param text:
        :return:
        """
        # join in case there are ":" values in answers and then split by ~
        text_list = ":".join(text).split("~")
        # find point ponder %100%, %30%, %0%...
        regex_point_ponder = re.compile("%(.*?)%")
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
            self.answers.append(Answer(points_ponder=point_ponder, value=value, comment=comment, tolerance=tolerance))

    def __str__(self):
        return "\n\nAnswer {}: ".format(self.__class__.__name__) + \
               "\n\tPoints: " + str(self.points) + \
               "\n\tSolution: " + str(self.answers)

    def __repr__(self):
        return self.__str__()

    def solve(self, solution):
        raise NotImplementedError


class ShortSolution(Solution):
    # TODO: solve * as a wildcard for all incorrect answers
    pass


class ShortSolutionC(ShortSolution):
    pass


class Numerical(Solution):
    def solve(self, solution):
        found_solution = False
        for sol in self.answers:
            # if correct answer is found
            if sol.value != "*" and float(sol.value) - float(sol.tolerance) <= solution <= float(sol.value) + float(sol.tolerance):
                return sol.points_ponder * self.points
        # if correct answer is not found and * has it's own point ponder
        if not found_solution and "*" in [x.value for x in self.answers]:
            return sol.points_ponder * self.points
        return 0


class Multichoice(Solution):
    pass


class Multiresponse(Solution):
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
    "SA": ShortSolution,
    "SAC": ShortSolutionC,
    "NM": Numerical,
    "MC": Multichoice,
    "MCV": Multichoice,
    "MCH": Multichoice,
    "MR": Multiresponse,
    "MRH": Multiresponse,
}

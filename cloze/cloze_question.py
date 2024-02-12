from dataclasses import dataclass, field

from cloze.cloze import Cloze, RenderType
from cloze.templates import html_render_template
from cloze.templates.cloze_render_template import fill_numerical


@dataclass
class ClozeAnswer(Cloze):
    answer_text: str
    ponder: float = 1.0
    feedback: str = None
    tolerance: float = None
    is_correct: bool = None


@dataclass
class ClozeResponse(Cloze):
    points_worth: int
    possible_answers: list[ClozeAnswer] = field(default_factory=list)
    question_type: str = None

    def add_possible_answer(self, answer: ClozeAnswer):
        self.possible_answers.append(answer)

    def export_cloze_response(self) -> str:
        return fill_numerical(question_type=self.question_type, points=self.points_worth, answers=self.possible_answers)


class Numerical(ClozeResponse):
    question_type = field(default="NUMERICAL")

    def add_possible_answer(self, answer: ClozeAnswer):
        float(answer.answer_text)  # check if answer text is number-like
        super(Numerical, self).add_possible_answer(answer)


class Multichoice(ClozeResponse):
    question_type: str
    ...


@dataclass
class ClozeQuestion(Cloze):
    question_text: str
    responses: list[ClozeResponse] = field(default_factory=list)

    def fill_question_parameters(self, *args, **kwargs):
        self.question_text = self.question_text.format(*args, **kwargs)

    def add_response(self, response: ClozeResponse):
        self.responses.append(response)

    def export_cloze_question(self) -> str:
        responses_text = ""
        for response in self.responses:
            responses_text += response.export_cloze_response()
        return responses_text

    def render(self, render_type: RenderType = RenderType.HTML):
        if render_type == RenderType.HTML:
            if not self._is_running_in_jupyter() and False:
                return "Can't render because not running in Jupyter"
            from IPython import display

            rendered_template = html_render_template.render_html(self)
            return display.HTML(rendered_template)

        elif render_type == RenderType.PLAIN:
            return "This is plain text render"

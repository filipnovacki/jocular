from jinja2 import Template

numerical_response_template = Template("""\
{ {{- points -}} : {{- question_type -}} : 
{%- for answer in answers -%} 
    ~ 
    {%- if answer.points_ponder -%} 
        % {{- (answer.points_ponder * 100) | int -}} % 
    {%- endif -%} 
    {{- answer.value -}} : {{- answer.tolerance -}} 
    {%- if answer.comment -%}
        # {{- answer.comment -}} 
    {%- endif -%}
{%- endfor -%} 
}""")


def fill_numerical(catch_wrong=False, points=None, answers=None, **kwargs):
    """
    Fills NUMERICAL template with values provided. Returns string.

    :param answers: (array of dicts):
        - value
        - point_ponder (optional)
        - tolerance (optional)
        - comment (optional)
    :param points: weight of the answer
    :param catch_wrong: bool, should all wrong answers be caught. Defaults to False
    :param kwargs:
    :return: string of rendered answers
    """
    return numerical_response_template.render(
        question_type="NUMERICAL",
        catch_wrong=catch_wrong,
        points=points,
        answers=answers,
        **kwargs
    )



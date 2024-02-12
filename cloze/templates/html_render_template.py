from jinja2 import Template

from cloze.cloze import Cloze

template = Template("""
<p><em>Pitanje: </em> {{ question_text }} </p>
{% if responses %}
    <em>Odgovori</em><br>
    {% for response in responses -%}
        <ul>
        {% for possible_answer in response.possible_answers -%}
            <li> 
                {%- if possible_answer.is_correct %} <b> {% endif -%}
                {%- if response.question_type == "NUMERICAL" %} \\( {% endif -%}
                    {{ possible_answer.answer_text }} + y 
                {%- if response.question_type == "NUMERICAL" %} \\) {% endif -%}
                {% if possible_answer.feedback %} ({{ possible_answer.feedback }}) {% endif -%}
                {% if possible_answer.tolerance %} +-{{ possible_answer.tolerance }} {% endif -%}
                {%- if possible_answer.is_correct %} </b> {% endif -%}
            </li>        
        {% endfor -%}
        </ul><br>
    {% endfor %}
{% endif %}
""")


def render_html(question_instance: Cloze):
    render_fields = {}
    if question_text := getattr(question_instance, "question_text"):
        render_fields["question_text"] = question_text
    if responses := getattr(question_instance, "responses"):
        render_fields["responses"] = responses
    return template.render(render_fields)

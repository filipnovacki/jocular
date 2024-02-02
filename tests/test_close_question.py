from cloze.cloze_question import ClozeQuestion


def test_cloze_question_question_formatting():
    q = ClozeQuestion("Koliko je {} + {}?")
    assert q.question_text == "Koliko je {} + {}?"
    q.fill_question_parameters(5, 6)
    assert q.question_text == "Koliko je 5 + 6?"

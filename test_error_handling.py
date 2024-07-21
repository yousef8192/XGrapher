import pytest
from _XGRAPHER_MAIN_ import *
from PySide2 import QtCore # for button clicks


@pytest.fixture
def app(qtbot):
    window = XGrapherWindow(1920, 1080)
    qtbot.addWidget(window)
    yield window
    matplotlib.pyplot.close()   # to reduce total memory used by the test file and increase execution time




def test_input_without_equation(app, qtbot):
    app.equation_field.setText('')
    app.x_min_field.setText('10')
    app.x_max_field.setText('-10')
    successfully_graphed = plot_equation(app, app.equation_field.text(), app.x_min_field.text(), app.x_max_field.text())
    assert (successfully_graphed == False)

def test_input_with_garbage_equation(app, qtbot):
    app.equation_field.setText('blabla')
    app.x_min_field.setText('-100')
    app.x_max_field.setText('100')
    successfully_graphed = plot_equation(app, app.equation_field.text(), app.x_min_field.text(), app.x_max_field.text())
    assert (successfully_graphed == False)

def test_input_with_syntax_error_of_multiple_dots_in_the_same_number(app, qtbot):
    app.equation_field.setText('12.2.2*x')
    app.x_min_field.setText('-100')
    app.x_max_field.setText('100')
    successfully_graphed = plot_equation(app, app.equation_field.text(), app.x_min_field.text(), app.x_max_field.text())
    assert (successfully_graphed == False)

def test_input_with_syntax_error_of_not_using_the_asterik_for_multiply(app, qtbot):
    app.equation_field.setText('12x')
    app.x_min_field.setText('-100')
    app.x_max_field.setText('100')
    successfully_graphed = plot_equation(app, app.equation_field.text(), app.x_min_field.text(), app.x_max_field.text())
    assert (successfully_graphed == False)

def test_input_with_syntax_error_of_using_double_asterik_instead_of_cap_for_exponentiation(app, qtbot):
    app.equation_field.setText('12**x')
    app.x_min_field.setText('-100')
    app.x_max_field.setText('100')
    successfully_graphed = plot_equation(app, app.equation_field.text(), app.x_min_field.text(), app.x_max_field.text())
    assert (successfully_graphed == False)

def test_input_with_syntax_error_of_using_double_asterik_instead_of_cap_for_exponentiation(app, qtbot):
    app.equation_field.setText('12**x')
    app.x_min_field.setText('-100')
    app.x_max_field.setText('100')
    successfully_graphed = plot_equation(app, app.equation_field.text(), app.x_min_field.text(), app.x_max_field.text())
    assert (successfully_graphed == False)

def test_input_that_causes_overflow_due_to_an_extremly_rising_function(app, qtbot):
    app.equation_field.setText('x^99999')
    app.x_min_field.setText('-100')
    app.x_max_field.setText('100')
    successfully_graphed = plot_equation(app, app.equation_field.text(), app.x_min_field.text(), app.x_max_field.text())
    assert (successfully_graphed == False)


def test_input_that_causes_overflow_due_to_extremely_large_input_range(app, qtbot):
    app.equation_field.setText('x')
    app.x_min_field.setText('-1e99999')
    app.x_max_field.setText('1e99999')
    successfully_graphed = plot_equation(app, app.equation_field.text(), app.x_min_field.text(), app.x_max_field.text())
    assert (successfully_graphed == False)

def test_input_with_no_range_inputted(app, qtbot):
    app.equation_field.setText('x')
    app.x_min_field.setText('')
    app.x_max_field.setText('-10')
    successfully_graphed = plot_equation(app, app.equation_field.text(), app.x_min_field.text(), app.x_max_field.text())
    assert (successfully_graphed == False)

def test_input_with_garbage_range_inputted(app, qtbot):
    app.equation_field.setText('x')
    app.x_min_field.setText('adsklfj')
    app.x_max_field.setText('-10')
    successfully_graphed = plot_equation(app, app.equation_field.text(), app.x_min_field.text(), app.x_max_field.text())
    assert (successfully_graphed == False)

def test_input_with_syntax_error_in_range_inputted(app, qtbot):
    app.equation_field.setText('x')
    app.x_min_field.setText('123.456.789')
    app.x_max_field.setText('-10')
    successfully_graphed = plot_equation(app, app.equation_field.text(), app.x_min_field.text(), app.x_max_field.text())
    assert (successfully_graphed == False)

def test_input_with_reversed_x_min_and_x_max(app, qtbot):
    app.equation_field.setText('x')
    app.x_min_field.setText('10')
    app.x_max_field.setText('-10')
    successfully_graphed = plot_equation(app, app.equation_field.text(), app.x_min_field.text(), app.x_max_field.text())
    assert (successfully_graphed == False)











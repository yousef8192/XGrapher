import pytest
from _XGRAPHER_MAIN_ import *
from PySide2 import QtCore # for button clicks


@pytest.fixture
def app(qtbot):
    window = XGrapherWindow(1920, 1080)
    qtbot.addWidget(window)
    yield window
    matplotlib.pyplot.close()   # to reduce total memory used by the test file and increase execution time




def test_graph_function_linear(app, qtbot):
    app.equation_field.setText('x')
    app.x_min_field.setText('-100')
    app.x_max_field.setText('100')
    successfully_graphed = plot_equation(app, app.equation_field.text(), app.x_min_field.text(), app.x_max_field.text())
    assert (successfully_graphed == True)

def test_graph_function_constant(app, qtbot):
    app.equation_field.setText('-5')
    app.x_min_field.setText('-100')
    app.x_max_field.setText('100')
    successfully_graphed = plot_equation(app, app.equation_field.text(), app.x_min_field.text(), app.x_max_field.text())
    assert (successfully_graphed == True)

def test_graph_function_x_over_x(app, qtbot):
    app.equation_field.setText('x/x')
    app.x_min_field.setText('-100')
    app.x_max_field.setText('100')
    successfully_graphed = plot_equation(app, app.equation_field.text(), app.x_min_field.text(), app.x_max_field.text())
    assert (successfully_graphed == True)

def test_graph_function_with_exponentiation_operator(app, qtbot):
    app.equation_field.setText('x^2')
    app.x_min_field.setText('-100')
    app.x_max_field.setText('100')
    successfully_graphed = plot_equation(app, app.equation_field.text(), app.x_min_field.text(), app.x_max_field.text())
    assert (successfully_graphed == True)

def test_graph_function_with_multiple_exponentiation_operator(app, qtbot):
    app.equation_field.setText('x^2 + x^3 + x^4 + x^5')
    app.x_min_field.setText('-100')
    app.x_max_field.setText('100')
    successfully_graphed = plot_equation(app, app.equation_field.text(), app.x_min_field.text(), app.x_max_field.text())
    assert (successfully_graphed == True)

def test_graph_function_with_no_asymptotic_points(app, qtbot):
    app.equation_field.setText('x')
    app.x_min_field.setText('-100')
    app.x_max_field.setText('100')
    successfully_graphed = plot_equation(app, app.equation_field.text(), app.x_min_field.text(), app.x_max_field.text())
    assert (successfully_graphed == True)

def test_graph_function_with_one_asymptotic_point(app, qtbot):
    app.equation_field.setText('1/x')
    app.x_min_field.setText('-10')
    app.x_max_field.setText('10')
    successfully_graphed = plot_equation(app, app.equation_field.text(), app.x_min_field.text(), app.x_max_field.text())
    assert (successfully_graphed == True)

def test_graph_function_with_two_asymptotic_points(app, qtbot):
    app.equation_field.setText('1/((x-2)*(x+2))')
    app.x_min_field.setText('-10')
    app.x_max_field.setText('10')
    successfully_graphed = plot_equation(app, app.equation_field.text(), app.x_min_field.text(), app.x_max_field.text())
    assert (successfully_graphed == True)

def test_graph_function_with_three_asymptotic_points(app, qtbot):
    app.equation_field.setText('1/((x-2)*(x-55)*(x-100))')
    app.x_min_field.setText('-1000')
    app.x_max_field.setText('1000')
    successfully_graphed = plot_equation(app, app.equation_field.text(), app.x_min_field.text(), app.x_max_field.text())
    assert (successfully_graphed == True)

def test_graph_function_sqrt_in_positive_interval(app, qtbot):
    app.equation_field.setText('sqrt(x)')
    app.x_min_field.setText('0')
    app.x_max_field.setText('10')
    successfully_graphed = plot_equation(app, app.equation_field.text(), app.x_min_field.text(), app.x_max_field.text())
    assert (successfully_graphed == True)

def test_graph_function_sqrt_in_negative_interval(app, qtbot):
    app.equation_field.setText('sqrt(x)')
    app.x_min_field.setText('-10')
    app.x_max_field.setText('-1')
    successfully_graphed = plot_equation(app, app.equation_field.text(), app.x_min_field.text(), app.x_max_field.text())
    assert (successfully_graphed == False)

def test_graph_function_sqrt_in_negative_and_positive_interval(app, qtbot):
    app.equation_field.setText('sqrt(x)')
    app.x_min_field.setText('-10')
    app.x_max_field.setText('10')
    successfully_graphed = plot_equation(app, app.equation_field.text(), app.x_min_field.text(), app.x_max_field.text())
    assert (successfully_graphed == True)

def test_graph_function_log10_in_positive_interval(app, qtbot):
    app.equation_field.setText('log10(x)')
    app.x_min_field.setText('0')
    app.x_max_field.setText('10')
    successfully_graphed = plot_equation(app, app.equation_field.text(), app.x_min_field.text(), app.x_max_field.text())
    assert (successfully_graphed == True)

def test_graph_function_log10_in_negative_interval(app, qtbot):
    app.equation_field.setText('log10(x)')
    app.x_min_field.setText('-10')
    app.x_max_field.setText('-1')
    successfully_graphed = plot_equation(app, app.equation_field.text(), app.x_min_field.text(), app.x_max_field.text())
    assert (successfully_graphed == False)

def test_graph_function_log10_in_negative_and_positive_interval(app, qtbot):
    app.equation_field.setText('log10(x)')
    app.x_min_field.setText('-10')
    app.x_max_field.setText('10')
    successfully_graphed = plot_equation(app, app.equation_field.text(), app.x_min_field.text(), app.x_max_field.text())
    assert (successfully_graphed == True)


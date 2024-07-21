import pytest
from xgrapher import *
from PySide2 import QtCore # for button clicks


# please notice that each time a gui window instance is instantiated, a direcotry named __PYCACHE__ is created with a file named test_...
# this file slows down the execution of the test attempts (deleting the file/directory is useless since it will be created again during execution)
# Thus it is recommended to insert a terminating character (such as ctrl+c in bash) to abort testing of this file and continue with the tests in interest


@pytest.fixture
def app(qtbot):
    window = XGrapherWindow(1920, 1080)
    qtbot.addWidget(window)
    yield window
    matplotlib.pyplot.close()   # to reduce total memory used by the test file and increase execution time












######################################################################################### Logic Functions Test




def test_compute_domain_one_over_x(app, qtbot):
    equation = '1/x'
    domain_returned = compute_domain(equation)
    assert (domain_returned == 'Union(Interval.open(-oo, 0), Interval.open(0, oo))')

def test_compute_intersection_non_intersecting_sets(app, qtbot):
    set_1 = "Interval(-100, -1)"
    set_2 = "Interval(1, 100)"
    intersection = compute_intersection(set_1, set_2)
    assert (intersection == ['EmptySet'])

def test_compute_asymptotic_points_for_interval_with_two_asymptotic_points(app, qtbot):
    test_list = [-100, 1, 1, 2, 2, 100]
    asymptotic_points = compute_asymptotic_points(test_list)
    assert (asymptotic_points == [1, 2])

def test_compute_asymptotic_points_for_interval_with_no_asymptotic_points(app, qtbot):
    test_list = [-100, 100]
    asymptotic_points = compute_asymptotic_points(test_list)
    assert (asymptotic_points == [])

def test_compute_asymptotic_points_for_invalid_interval(app, qtbot):
    test_list = []
    asymptotic_points = compute_asymptotic_points(test_list)
    assert (asymptotic_points == [])

def test_insert_asymptotic_points_that_already_exist(app, qtbot):
    test_asymptotic_points_list = [2, 5]
    test_x_points_intersection_range = [1, 2, 3, 4, 5]
    test_y_points_intersection_range = [1, 2, 3, 4, 5]
    insert_asymptotic_points(test_asymptotic_points_list, test_x_points_intersection_range, test_y_points_intersection_range)
    assert ((test_x_points_intersection_range == [1, 2, 3, 4, 5]) and (test_y_points_intersection_range == [1, 2, 3, 4, 5]))

def test_insert_asymptotic_points_that_do_not_exist(app, qtbot):
    test_asymptotic_points_list = [2, 5]
    test_x_points_intersection_range = [1, 3, 4]
    test_y_points_intersection_range = [1, 3, 4]
    insert_asymptotic_points(test_asymptotic_points_list, test_x_points_intersection_range, test_y_points_intersection_range)
    assert ((test_x_points_intersection_range == [1, 2, 3, 4, 5]) and (test_y_points_intersection_range == [1, numpy.nan, 3, 4, numpy.nan]))

def test_insert_fitting_points(app, qtbot):
    test_asymptotic_points_list = [2, 5]
    test_x_points_intersection_range = [1, 2, 3, 4, 5]
    test_y_points_intersection_range = [1, numpy.nan, 3, 4, numpy.nan]
    test_equation_exec = '1/((x-2)*(x-5))'

    old_x_points_len = len(test_x_points_intersection_range)
    old_y_points_len = len(test_y_points_intersection_range)
    num_asym_points = len(test_asymptotic_points_list)
    num_points_to_add = num_asym_points * 50

    insert_fitting_points(test_asymptotic_points_list, test_x_points_intersection_range, test_y_points_intersection_range, test_equation_exec)

    new_x_points_len = len(test_x_points_intersection_range)
    new_y_points_len = len(test_y_points_intersection_range)

    assert ((new_x_points_len==(old_x_points_len+num_points_to_add)) and (new_y_points_len==(old_y_points_len+num_points_to_add)))











######################################################################################### Input Sanitization and Error Handling Tests




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






######################################################################################### Curve Plotting Tests

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









######################################################################################### Curve Plotting Tests




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


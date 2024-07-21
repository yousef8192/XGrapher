import pytest
from _XGRAPHER_MAIN_ import *
from PySide2 import QtCore # for button clicks


@pytest.fixture
def app(qtbot):
    window = XGrapherWindow(1920, 1080)
    qtbot.addWidget(window)
    yield window
    matplotlib.pyplot.close()   # to reduce total memory used by the test file and increase execution time






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

def test_update_min_max_coordinates(app, qtbot):
     
    app.min_y_in_graph = -100
    app.max_y_in_graph = 100
    app.min_x_in_graph = -100
    app.max_x_in_graph = 100

    old_min_y_in_graph = app.min_y_in_graph
    old_max_y_in_graph = app.max_y_in_graph
    old_min_x_in_graph = app.min_x_in_graph
    old_max_x_in_graph = app.max_x_in_graph

    a = old_min_x_in_graph-10
    b = old_max_x_in_graph+10
    c = b-a
    d = old_min_y_in_graph-10
    e = old_max_y_in_graph+10
    f = e-d

    x_points_intersection_range = [a, b]
    y_points_intersection_range = [d, e]

    update_min_max_coordinates(app, x_points_intersection_range, y_points_intersection_range)

    assert ((app.min_y_in_graph==d-0.1*f) and (app.max_y_in_graph==e+0.1*f) and (app.min_x_in_graph==a-0.1*c) and (app.max_x_in_graph==b+0.1*c))






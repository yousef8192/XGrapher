import pytest
from _XGRAPHER_MAIN_ import *
from PySide2 import QtCore # for button clicks


@pytest.fixture
def app(qtbot):
    window = XGrapherWindow(1920, 1080)
    qtbot.addWidget(window)
    yield window
    matplotlib.pyplot.close()   # to reduce total memory used by the test file and increase execution time












######################################################################################### Logic Functions Test




def test_application_initialization(app):
    assert app.status_bar.currentMessage() == "Welcome to XGrapher!! Please insert an equation to plot..."

def test_keypad_insertion_buttons(app, qtbot):
    qtbot.mouseClick(app.button_x, QtCore.Qt.LeftButton)
    qtbot.mouseClick(app.button_1, QtCore.Qt.LeftButton)
    assert app.equation_field.text() == "x1"

def test_keypad_delete_button(app, qtbot):
    app.equation_field.setText('test string')
    qtbot.mouseClick(app.button_del, QtCore.Qt.LeftButton)
    assert app.equation_field.text() == 'test strin'

def test_keypad_clear_button(app, qtbot):
    app.equation_field.setText('test string')
    qtbot.mouseClick(app.button_clear, QtCore.Qt.LeftButton)
    assert app.equation_field.text() == ''

def test_keypad_sqrt_button(app, qtbot):
    qtbot.mouseClick(app.button_sqrt, QtCore.Qt.LeftButton)
    assert app.equation_field.text() == 'sqrt()'

def test_keypad_navigation_buttons(app, qtbot):
    app.equation_field.setText('test string')
    qtbot.mouseClick(app.button_left, QtCore.Qt.LeftButton)
    qtbot.mouseClick(app.button_x, QtCore.Qt.LeftButton)
    qtbot.mouseClick(app.button_right, QtCore.Qt.LeftButton)
    qtbot.mouseClick(app.button_x, QtCore.Qt.LeftButton)
    assert app.equation_field.text() == 'test strinxgx'


# It is preferred to have separate file for the imports 
# since as the project grows and uses more libraries and frameworks, the
# imports will bloat the file which might be a bit annoying for the developers
from _XGRAPHER_GUI_IMPORTS_ import * 

# This is the main class that creates the window for the XGrapher application 
# This class contains all the gui related objects and methods needed for the application to operate
class XGrapherWindow(QMainWindow):

    # constructor of the XGrapherWindow class
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        super().__init__()

        self.main_widget = QWidget()
        self.main_widget.setLayout(QGridLayout())
        self.setCentralWidget(self.main_widget)

        self.setWindowTitle('XGrapher')
        self.setWindowIcon(QIcon(os.path.join('img', 'XGrapher_icon.png')))
        self.setMinimumSize(0.71*SCREEN_WIDTH, 0.65*SCREEN_HEIGHT)
        self.resize(0.71*SCREEN_WIDTH, 0.65*SCREEN_HEIGHT)
 

        self.create_keypad() 
        self.create_range_fields() 
        self.create_axes() 
        self.create_y_range_slider()
        self.create_x_range_slider()

        self.create_tool_bar()
        self.create_status_bar()

        self.graphical_mode = 1  # light mode
        self.set_graphical_mode(self.graphical_mode)


    def create_tool_bar(self):

        self.tool_bar = NavigationToolbar2QT(self.canvas, self)

        self.light_mode_action = QAction(QIcon(os.path.join('img', 'light_mode.svg')), "Light Mode", self)
        self.dark_mode_action = QAction(QIcon(os.path.join('img', 'dark_mode.svg')), "Dark Mode", self)

        self.light_mode_action.triggered.connect(lambda : self.set_graphical_mode(1))
        self.dark_mode_action.triggered.connect(lambda : self.set_graphical_mode(0))

        self.tool_bar.addAction(self.light_mode_action)
        self.tool_bar.addAction(self.dark_mode_action)

        self.addToolBar(self.tool_bar)


    def create_status_bar(self):
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Welcome to XGrapher!! Please insert an equation to plot...")
        self.status_bar.timer = QTimer(self)        # create a timer for the status bar
        self.status_bar.timer.setSingleShot(True)   # set the timer to run only once (not periodically) to avoid wasting cpu resources
        self.status_bar.setStyleSheet("font-size: 24px; font-weight:600; color:#CECECE; background-color:#2D2D2D; border:1.2px solid #707070")


    def create_keypad(self):

        self.keypad_container = QWidget()
        self.keypad_container.setLayout(QGridLayout())

        # added self. before result_field since will need to use it outside of this method
        self.equation_field   = QLineEdit()
        self.equation_field.setPlaceholderText("Enter the Equation...")
        self.equation_field.setAlignment(Qt.AlignLeft)
        self.equation_field.returnPressed.connect(lambda : graph_equation(self, self.equation_field.text(), self.x_min_field.text(), self.x_max_field.text()))

        self.button_graph        = QPushButton('Graph',      clicked = lambda : (graph_equation(self, self.equation_field.text(), self.x_min_field.text(), self.x_max_field.text()),
                                                                            self.equation_field.setFocus(),
                                                                            self.equation_field.clearFocus()))

        self.button_equal        = QPushButton('=',          clicked = lambda : (graph_equation(self, self.equation_field.text(), self.x_min_field.text(), self.x_max_field.text()),
                                                                            self.equation_field.setFocus(),
                                                                            self.equation_field.clearFocus()))

        self.button_sqrt         = QPushButton('sqrt()',     clicked = lambda: (self.equation_field.insert('sqrt()'),
                                                                           self.equation_field.cursorBackward(False,1),
                                                                           self.equation_field.setFocus()) )

        self.button_log10        = QPushButton('log10()',    clicked = lambda: (self.equation_field.insert('log10()'),
                                                                           self.equation_field.cursorBackward(False,1),
                                                                           self.equation_field.setFocus()))

        self.button_del          = QPushButton('Del',        clicked = lambda: (self.equation_field.backspace(),self.equation_field.setFocus())              )
        self.button_clear        = QPushButton('Clear',      clicked = lambda: (self.equation_field.clear(),self.equation_field.setFocus())                  )
        self.button_left         = QPushButton('←',          clicked = lambda: (self.equation_field.cursorBackward(False,1),self.equation_field.setFocus())  )
        self.button_right        = QPushButton('→',          clicked = lambda: (self.equation_field.cursorForward(False,1),self.equation_field.setFocus())   )
        self.button_x            = QPushButton('x',          clicked = lambda: (self.equation_field.insert('x'),self.equation_field.setFocus())              )
        self.button_sub          = QPushButton('-',          clicked = lambda: (self.equation_field.insert('-'),self.equation_field.setFocus())              )
        self.button_add          = QPushButton('+',          clicked = lambda: (self.equation_field.insert('+'),self.equation_field.setFocus())              )
        self.button_mul          = QPushButton('*',          clicked = lambda: (self.equation_field.insert('*'),self.equation_field.setFocus())              )
        self.button_exp          = QPushButton('^',          clicked = lambda: (self.equation_field.insert('^'),self.equation_field.setFocus())              )
        self.button_div          = QPushButton('/',          clicked = lambda: (self.equation_field.insert('/'),self.equation_field.setFocus())              )
        self.button_open_paren   = QPushButton('(',          clicked = lambda: (self.equation_field.insert('('),self.equation_field.setFocus())              )
        self.button_close_paren  = QPushButton(')',          clicked = lambda: (self.equation_field.insert(')'),self.equation_field.setFocus())              )
        self.button_7            = QPushButton('7',          clicked = lambda: (self.equation_field.insert('7'),self.equation_field.setFocus())              )
        self.button_8            = QPushButton('8',          clicked = lambda: (self.equation_field.insert('8'),self.equation_field.setFocus())              )
        self.button_9            = QPushButton('9',          clicked = lambda: (self.equation_field.insert('9'),self.equation_field.setFocus())              )
        self.button_4            = QPushButton('4',          clicked = lambda: (self.equation_field.insert('4'),self.equation_field.setFocus())              )
        self.button_5            = QPushButton('5',          clicked = lambda: (self.equation_field.insert('5'),self.equation_field.setFocus())              )
        self.button_6            = QPushButton('6',          clicked = lambda: (self.equation_field.insert('6'),self.equation_field.setFocus())              )
        self.button_1            = QPushButton('1',          clicked = lambda: (self.equation_field.insert('1'),self.equation_field.setFocus())              )
        self.button_2            = QPushButton('2',          clicked = lambda: (self.equation_field.insert('2'),self.equation_field.setFocus())              )
        self.button_3            = QPushButton('3',          clicked = lambda: (self.equation_field.insert('3'),self.equation_field.setFocus())              )
        self.button_0            = QPushButton('0',          clicked = lambda: (self.equation_field.insert('0'),self.equation_field.setFocus())              )
        self.button_dot          = QPushButton('.',          clicked = lambda: (self.equation_field.insert('.'),self.equation_field.setFocus())              )


        self.button_graph.setSizePolicy(                     QSizePolicy.Expanding, QSizePolicy.Expanding )
        self.button_equal.setSizePolicy(                     QSizePolicy.Expanding, QSizePolicy.Expanding )
        self.button_del.setSizePolicy(                       QSizePolicy.Expanding, QSizePolicy.Expanding )
        self.button_clear.setSizePolicy(                     QSizePolicy.Expanding, QSizePolicy.Expanding )
        self.button_left.setSizePolicy(                      QSizePolicy.Expanding, QSizePolicy.Expanding )
        self.button_right.setSizePolicy(                     QSizePolicy.Expanding, QSizePolicy.Expanding )
        self.button_x.setSizePolicy(                         QSizePolicy.Expanding, QSizePolicy.Expanding )
        self.button_sub.setSizePolicy(                       QSizePolicy.Expanding, QSizePolicy.Expanding )
        self.button_add.setSizePolicy(                       QSizePolicy.Expanding, QSizePolicy.Expanding )
        self.button_mul.setSizePolicy(                       QSizePolicy.Expanding, QSizePolicy.Expanding )
        self.button_exp.setSizePolicy(                       QSizePolicy.Expanding, QSizePolicy.Expanding )
        self.button_div.setSizePolicy(                       QSizePolicy.Expanding, QSizePolicy.Expanding )
        self.button_sqrt.setSizePolicy(                      QSizePolicy.Expanding, QSizePolicy.Expanding )
        self.button_log10.setSizePolicy(                     QSizePolicy.Expanding, QSizePolicy.Expanding )
        self.button_open_paren.setSizePolicy(                QSizePolicy.Expanding, QSizePolicy.Expanding )
        self.button_close_paren.setSizePolicy(               QSizePolicy.Expanding, QSizePolicy.Expanding )
        self.button_7.setSizePolicy(                         QSizePolicy.Expanding, QSizePolicy.Expanding )
        self.button_8.setSizePolicy(                         QSizePolicy.Expanding, QSizePolicy.Expanding )
        self.button_9.setSizePolicy(                         QSizePolicy.Expanding, QSizePolicy.Expanding )
        self.button_4.setSizePolicy(                         QSizePolicy.Expanding, QSizePolicy.Expanding )
        self.button_5.setSizePolicy(                         QSizePolicy.Expanding, QSizePolicy.Expanding )
        self.button_6.setSizePolicy(                         QSizePolicy.Expanding, QSizePolicy.Expanding )
        self.button_1.setSizePolicy(                         QSizePolicy.Expanding, QSizePolicy.Expanding )
        self.button_2.setSizePolicy(                         QSizePolicy.Expanding, QSizePolicy.Expanding )
        self.button_3.setSizePolicy(                         QSizePolicy.Expanding, QSizePolicy.Expanding )
        self.button_0.setSizePolicy(                         QSizePolicy.Expanding, QSizePolicy.Expanding )
        self.button_dot.setSizePolicy(                       QSizePolicy.Expanding, QSizePolicy.Expanding )


        self.keypad_container.layout().addWidget( self.equation_field,      0, 0, 1, 3 )

        self.keypad_container.layout().addWidget( self.button_left,         1, 0, 1, 1 )
        self.keypad_container.layout().addWidget( self.button_right,        1, 1, 1, 1 )
        self.keypad_container.layout().addWidget( self.button_x,            1, 2, 1, 1 )

        self.keypad_container.layout().addWidget( self.button_del,          2, 0, 1, 1 )
        self.keypad_container.layout().addWidget( self.button_clear,        2, 1, 1, 1 )
        self.keypad_container.layout().addWidget( self.button_graph,        2, 2, 1, 1 )

        self.keypad_container.layout().addWidget( self.button_log10,        3, 0, 1, 1 )
        self.keypad_container.layout().addWidget( self.button_sqrt,         3, 1, 1, 1 )
        self.keypad_container.layout().addWidget( self.button_exp,          3, 2, 1, 1 )

        self.keypad_container.layout().addWidget( self.button_open_paren,   4, 0, 1, 1 )
        self.keypad_container.layout().addWidget( self.button_close_paren,  4, 1, 1, 1 )
        self.keypad_container.layout().addWidget( self.button_div,          4, 2, 1, 1 )

        self.keypad_container.layout().addWidget( self.button_mul,          5, 0, 1, 1 )
        self.keypad_container.layout().addWidget( self.button_sub,          5, 1, 1, 1 )
        self.keypad_container.layout().addWidget( self.button_add,          5, 2, 1, 1 )

        self.keypad_container.layout().addWidget( self.button_7,            6, 0, 1, 1 )
        self.keypad_container.layout().addWidget( self.button_8,            6, 1, 1, 1 )
        self.keypad_container.layout().addWidget( self.button_9,            6, 2, 1, 1 )

        self.keypad_container.layout().addWidget( self.button_4,            7, 0, 1, 1 )
        self.keypad_container.layout().addWidget( self.button_5,            7, 1, 1, 1 )
        self.keypad_container.layout().addWidget( self.button_6,            7, 2, 1, 1 )

        self.keypad_container.layout().addWidget( self.button_1,            8, 0, 1, 1 )
        self.keypad_container.layout().addWidget( self.button_2,            8, 1, 1, 1 )
        self.keypad_container.layout().addWidget( self.button_3,            8, 2, 1, 1 )

        self.keypad_container.layout().addWidget( self.button_0,            9, 0, 1, 1 )
        self.keypad_container.layout().addWidget( self.button_dot,          9, 1, 1, 1 )
        self.keypad_container.layout().addWidget( self.button_equal,        9, 2, 1, 1 )

        self.main_widget.layout().addWidget(self.keypad_container,          0, 0, 1, 1)

        


    def create_range_fields(self):

        self.x_min_label = QLabel("Minimum value for x :  ")
        self.x_min_field = QLineEdit()
        self.x_min_field.setAlignment(Qt.AlignCenter) 
        self.x_min_field.setPlaceholderText(".......")
        self.x_min_field.returnPressed.connect(lambda : graph_equation(self, self.equation_field.text(), self.x_min_field.text(), self.x_max_field.text()))
        self.x_min_label_input = QWidget()
        self.x_min_label_input.setLayout(QGridLayout())
        self.x_min_label_input.layout().addWidget(self.x_min_label,        0, 0, 1, 1 )
        self.x_min_label_input.layout().addWidget(self.x_min_field,        0, 1, 1, 2 )

        self.x_max_label = QLabel("Maximum value for x :  ")
        self.x_max_field = QLineEdit()
        self.x_max_field.setAlignment(Qt.AlignCenter) 
        self.x_max_field.setPlaceholderText(".......")
        self.x_max_field.returnPressed.connect(lambda : graph_equation(self, self.equation_field.text(), self.x_min_field.text(), self.x_max_field.text()))
        self.x_max_label_input = QWidget()
        self.x_max_label_input.setLayout(QGridLayout())
        self.x_max_label_input.layout().addWidget(self.x_max_label,        0, 0, 1, 1 )
        self.x_max_label_input.layout().addWidget(self.x_max_field,        0, 1, 1, 2 )

        self.keypad_container.layout().addWidget(self.x_min_label_input,   10, 0, 1, 3)
        self.keypad_container.layout().addWidget(self.x_max_label_input,   11, 0, 1, 3)


    def create_axes(self):
        
        self.min_y_in_graph = -0.05
        self.max_y_in_graph = 0.05
        self.min_x_in_graph = -0.05
        self.max_x_in_graph = 0.05

        self.figure = matplotlib.pyplot.figure(figsize=(8, 4))
        self.canvas = FigureCanvas(self.figure)
        self.graph  = self.figure.add_subplot()

        self.graph.grid(True)
        self.graph.set_title("Title", fontsize=18)
        self.graph.set_xlabel("X-Label", fontsize=18)
        self.graph.set_ylabel("Y-Label", fontsize=18)
        self.graph.plot()
        self.x_axis = self.graph.axhline(y=0, color='#000000', linewidth=1)
        self.y_axis = self.graph.axvline(x=0, color='#000000', linewidth=1)

        self.legend = self.graph.legend('', loc='upper left')
        self.legend.set_visible(False) 

        self.main_widget.layout().addWidget(self.canvas, 0, 4, 1, 1)


    def create_y_range_slider(self):

        self.y_range_slider = QSlider(Qt.Vertical)
        self.y_range_slider.setMinimum(1)
        self.y_range_slider.setMaximum(10000)
        self.y_range_slider.setValue(1000)
        
        self.y_range_slider.valueChanged.connect(self.y_range_slider_slot)

        self.main_widget.layout().setColumnMinimumWidth(1,25)   # separator of width 25px
        self.main_widget.layout().addWidget(self.y_range_slider, 0, 2, 1, 1)
        self.main_widget.layout().setColumnMinimumWidth(3,5)   # separator of width 5px


    def create_x_range_slider(self):

        self.x_range_slider = QSlider(Qt.Horizontal)
        self.x_range_slider.setMinimum(1)
        self.x_range_slider.setMaximum(10000)
        self.x_range_slider.setValue(1000)
        
        self.x_range_slider.valueChanged.connect(self.x_range_slider_slot)

        self.main_widget.layout().addWidget(self.x_range_slider, 1, 4, 1, 1)


    # The algorithm of the slot is that it centers the plot according to the minimum and maximum y points among all the curves in the plot 
    # Then the y-zoom slider stretches and shrinks the y-axis accordingly
    # The minimum and maximum y points are being continuously updated by the update_min_max_coordinates() function each time a curve gets plotted
    def y_range_slider_slot(self):

        slider_value_inverted = self.y_range_slider.maximum() - self.y_range_slider.value() + 1    # the + 1 is to avoid falling down to 0
        slider_value_scaled   = slider_value_inverted/self.y_range_slider.maximum()
        y_mid                 = (self.min_y_in_graph + self.max_y_in_graph)/2
        y_half_range          = (self.max_y_in_graph - self.min_y_in_graph)/2
        y_min_new             = y_mid - slider_value_scaled*y_half_range
        y_max_new             = y_mid + slider_value_scaled*y_half_range

        self.graph.set_ylim(y_min_new, y_max_new)
        self.canvas.draw()


    # The algorithm of the slot is that it centers the plot according to the minimum and maximum x points among all the curves in the plot 
    # Then the x-zoom slider stretches and shrinks the x-axis accordingly
    # The minimum and maximum x points are being continuously updated by the update_min_max_coordinates() function each time a curve gets plotted
    def x_range_slider_slot(self):

        slider_value_inverted = self.x_range_slider.maximum() - self.x_range_slider.value() + 1    # the + 1 is to avoid falling down to 0
        slider_value_scaled   = slider_value_inverted/self.x_range_slider.maximum()
        x_mid                 = (self.min_x_in_graph + self.max_x_in_graph)/2
        x_half_range          = (self.max_x_in_graph - self.min_x_in_graph)/2
        x_min_new             = x_mid - slider_value_scaled*x_half_range
        x_max_new             = x_mid + slider_value_scaled*x_half_range

        self.graph.set_xlim(x_min_new, x_max_new)
        self.canvas.draw()


    def status_bar_print(self, message, status):
        # status == 0 : indicates Success
        # status < 0  : indicates Error
        # status > 0  : indicates Warning
        # if else implementation is preferred to python's switch statement for the sake of backward compatibility

        if self.graphical_mode > 0:
            bg_color = "#E2E2E2"
        else:
            bg_color = "#2D2D2D"
        
        if status < 0:
            self.status_bar.setStyleSheet("font-size: 24px; font-weight:600; color:#c21313; background-color:{}; border:1.2px solid #707070".format(bg_color));
        elif status > 0:
            self.status_bar.setStyleSheet("font-size: 24px; font-weight:600; color:#ad8e00; background-color:{}; border:1.2px solid #707070".format(bg_color));
        else:
            self.status_bar.setStyleSheet("font-size: 24px; font-weight:600; color:#06bf09; background-color:{}; border:1.2px solid #707070".format(bg_color));


        # The following Code displays a pop-up animation when status bar text changes
        self.status_bar.showMessage('')
        self.status_bar.timer.timeout.connect(lambda : self.status_bar.showMessage(message))
        self.status_bar.timer.start(50)


    # This function updates the legend, which is the area at the top left that displays the functions that are plotted
    def update_legend(self):


        self.legend = self.graph.legend(loc='upper left')
        if self.graphical_mode > 0:
            self.legend.get_frame().set_facecolor('#FFFFFF') 
            for text in self.legend.get_texts(): text.set_color('#000000')
        else:
            self.legend.get_frame().set_facecolor('#3A3A3A') 
            for text in self.legend.get_texts(): text.set_color('#CECECE')


    def set_graphical_mode(self, graphical_mode):
        # graphical_mode >  0   :   light mode
        # graphical_mode <= 0   :   dark mode

        self.graphical_mode = graphical_mode

        if graphical_mode > 0:
            self.setStyleSheet( "background-color: #FFFFFF;")
            self.tool_bar.setStyleSheet("background-color:#E2E2E2; border:1.2px solid #707070")
            status_bar_text_color = self.status_bar.palette().color(QPalette.Text).name()
            if (status_bar_text_color.upper() == '#CECECE'):
                self.status_bar.setStyleSheet("font-size: 24px; font-weight:600; color:#000000; background-color:#E2E2E2; border:1.2px solid #707070")
            else:
                self.status_bar.setStyleSheet("font-size: 24px; font-weight:600; color:{}; background-color:#E2E2E2; border:1.2px solid #707070".format(status_bar_text_color))

            self.figure.patch.set_facecolor("#FFFFFF")
            self.graph.set_facecolor("#FFFFFF")
            self.graph.set_title(self.graph.get_title(), fontsize=18 , color="#000000")
            self.graph.set_xlabel(self.graph.get_xlabel(), fontsize=18, color="#000000")
            self.graph.set_ylabel(self.graph.get_ylabel(), fontsize=18, color="#000000")
            self.x_axis.set_color("#000000")
            self.y_axis.set_color("#000000")
            self.graph.tick_params(axis='x', colors='#000000')
            self.graph.tick_params(axis='y', colors='#000000')
            self.legend.get_frame().set_facecolor('#FFFFFF') 
            for text in self.legend.get_texts(): text.set_color('#000000')
            self.canvas.draw() # refresh the graph

            self.x_min_label.setStyleSheet(         "font-size: 22px;")
            self.x_min_field.setStyleSheet(         "font-size: 20px;")
            self.x_max_label.setStyleSheet(         "font-size: 22px;")
            self.x_max_field.setStyleSheet(         "font-size: 20px;")

            self.equation_field.setStyleSheet(      "font-size: 20px;")

            self.button_graph.setStyleSheet(        "font-size: 20px;")
            self.button_equal.setStyleSheet(        "font-size: 20px;")
            self.button_del.setStyleSheet(          "font-size: 20px;")
            self.button_clear.setStyleSheet(        "font-size: 20px;")
            self.button_left.setStyleSheet(         "font-size: 20px;")
            self.button_right.setStyleSheet(        "font-size: 20px;")
            self.button_x.setStyleSheet(            "font-size: 20px;")
            self.button_sub.setStyleSheet(          "font-size: 20px;")
            self.button_add.setStyleSheet(          "font-size: 20px;")
            self.button_mul.setStyleSheet(          "font-size: 20px;")
            self.button_exp.setStyleSheet(          "font-size: 20px;")
            self.button_div.setStyleSheet(          "font-size: 20px;")
            self.button_sqrt.setStyleSheet(         "font-size: 20px;")
            self.button_log10.setStyleSheet(        "font-size: 20px;")
            self.button_open_paren.setStyleSheet(   "font-size: 20px;")
            self.button_close_paren.setStyleSheet(  "font-size: 20px;")
            self.button_7.setStyleSheet(            "font-size: 20px;")
            self.button_8.setStyleSheet(            "font-size: 20px;")
            self.button_9.setStyleSheet(            "font-size: 20px;")
            self.button_4.setStyleSheet(            "font-size: 20px;")
            self.button_5.setStyleSheet(            "font-size: 20px;")
            self.button_6.setStyleSheet(            "font-size: 20px;")
            self.button_1.setStyleSheet(            "font-size: 20px;")
            self.button_2.setStyleSheet(            "font-size: 20px;")
            self.button_3.setStyleSheet(            "font-size: 20px;")
            self.button_0.setStyleSheet(            "font-size: 20px;")
            self.button_dot.setStyleSheet(          "font-size: 20px;")


        else:
            self.setStyleSheet("background-color:#3A3A3A;")
            self.tool_bar.setStyleSheet("color:#CFCFCF; background-color:#2D2D2D; border:1.2px solid #707070")

            status_bar_text_color = self.status_bar.palette().color(QPalette.Text).name()
            if (status_bar_text_color.upper() == '#000000'):
                self.status_bar.setStyleSheet("font-size: 24px; font-weight:600; color:#CECECE; background-color:#2D2D2D; border:1.2px solid #707070")
            else:
                self.status_bar.setStyleSheet("font-size: 24px; font-weight:600; color:{}; background-color:#2D2D2D; border:1.2px solid #707070".format(status_bar_text_color))


            self.figure.patch.set_facecolor("#3A3A3A")
            self.graph.set_facecolor("#000000")
            self.graph.set_title(self.graph.get_title(), fontsize=18 , color="#CECECE")
            self.graph.set_xlabel(self.graph.get_xlabel(), fontsize=18, color="#CECECE")
            self.graph.set_ylabel(self.graph.get_ylabel(), fontsize=18, color="#CECECE")
            self.x_axis.set_color("#CCCCCC")
            self.y_axis.set_color("#CCCCCC")
            self.graph.tick_params(axis='x', colors='#CECECE')
            self.graph.tick_params(axis='y', colors='#CECECE')
            self.legend.get_frame().set_facecolor('#3A3A3A') 
            for text in self.legend.get_texts(): text.set_color('#CECECE')
            self.canvas.draw() # refresh the graph

            self.x_min_label.setStyleSheet(         "font-size: 22px; color:#CECECE")
            self.x_min_field.setStyleSheet(         "font-size: 20px; color:#CECECE; background-color:#2C2C2C")
            self.x_max_label.setStyleSheet(         "font-size: 22px; color:#CECECE")
            self.x_max_field.setStyleSheet(         "font-size: 20px; color:#CECECE; background-color:#2C2C2C")

            self.equation_field.setStyleSheet(      "font-size: 20px; color:#CECECE; background-color:#2C2C2C")

            self.button_graph.setStyleSheet(        "font-size: 20px; color:#CECECE;")
            self.button_equal.setStyleSheet(        "font-size: 20px; color:#CECECE;")
            self.button_del.setStyleSheet(          "font-size: 20px; color:#CECECE;")
            self.button_clear.setStyleSheet(        "font-size: 20px; color:#CECECE;")
            self.button_left.setStyleSheet(         "font-size: 20px; color:#CECECE;")
            self.button_right.setStyleSheet(        "font-size: 20px; color:#CECECE;")
            self.button_x.setStyleSheet(            "font-size: 20px; color:#CECECE;")
            self.button_sub.setStyleSheet(          "font-size: 20px; color:#CECECE;")
            self.button_add.setStyleSheet(          "font-size: 20px; color:#CECECE;")
            self.button_mul.setStyleSheet(          "font-size: 20px; color:#CECECE;")
            self.button_exp.setStyleSheet(          "font-size: 20px; color:#CECECE;")
            self.button_div.setStyleSheet(          "font-size: 20px; color:#CECECE;")
            self.button_sqrt.setStyleSheet(         "font-size: 20px; color:#CECECE;")
            self.button_log10.setStyleSheet(        "font-size: 20px; color:#CECECE;")
            self.button_open_paren.setStyleSheet(   "font-size: 20px; color:#CECECE;")
            self.button_close_paren.setStyleSheet(  "font-size: 20px; color:#CECECE;")
            self.button_7.setStyleSheet(            "font-size: 20px; color:#CECECE;")
            self.button_8.setStyleSheet(            "font-size: 20px; color:#CECECE;")
            self.button_9.setStyleSheet(            "font-size: 20px; color:#CECECE;")
            self.button_4.setStyleSheet(            "font-size: 20px; color:#CECECE;")
            self.button_5.setStyleSheet(            "font-size: 20px; color:#CECECE;")
            self.button_6.setStyleSheet(            "font-size: 20px; color:#CECECE;")
            self.button_1.setStyleSheet(            "font-size: 20px; color:#CECECE;")
            self.button_2.setStyleSheet(            "font-size: 20px; color:#CECECE;")
            self.button_3.setStyleSheet(            "font-size: 20px; color:#CECECE;")
            self.button_0.setStyleSheet(            "font-size: 20px; color:#CECECE;")
            self.button_dot.setStyleSheet(          "font-size: 20px; color:#CECECE;")






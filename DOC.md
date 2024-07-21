# XGrapher Documentation



<!-- {{{Table of Contents --> 

## Table of Contents

* [Table of Contents](#table-of-contents)
* [XGrapher Code Documentation (Logic Code)](#xgrapher-code-documentation-logic-code)
  * [1. plot_equation(...)](#1-plot_equation)
  * [2. process_inputs(...)](#2-process_inputs)
  * [3. update_min_max_coordinates(...)](#3-update_min_max_coordinates)
  * [4. compute_domain(...)](#4-compute_domain)
  * [5. compute_intersection(...)](#5-compute_intersection)
  * [6. compute_asymptotic_points(...)](#6-compute_asymptotic_points)
  * [7. insert_asymptotic_points(...)](#7-insert_asymptotic_points)
  * [8. insert_fitting_points(...)](#8-insert_fitting_points)
* [XGrapher Code Documentation (GUI Code)](#xgrapher-code-documentation-gui-code)
  * [1. __init__(...)](#1-__init__)
  * [2. create_tool_bar(...)](#2-create_tool_bar)
  * [3. create_status_bar(...)](#3-create_status_bar)
  * [4. create_keypad(...)](#4-create_keypad)
  * [5. create_range_fields(...)](#5-create_range_fields)
  * [6. create_graph(...)](#6-create_graph)
  * [7. create_y_zoom_slider(...)](#7-create_y_zoom_slider)
  * [8. create_x_zoom_slider(...)](#8-create_x_zoom_slider)
  * [9. y_zoom_slider_slot(...)](#9-y_zoom_slider_slot)
  * [10. x_zoom_slider_slot(...)](#10-x_zoom_slider_slot)
  * [11. status_bar_print(...)](#11-status_bar_print)
  * [12. update_legend(...)](#12-update_legend)
  * [13. set_graphical_mode(...)](#13-set_graphical_mode)


<br/>
<!-- }}} -->

<!-- {{{XGrapher Code Documentation (Logic Code)--> 
<br/>

## XGrapher Code Documentation (Logic Code)

1. plot_equation(...)
2. process_inputs(...)
3. update_min_max_coordinates(...)
4. compute_domain(...)
5. compute_intersection(...)
6. compute_asymptotic_points(...)
7. insert_asymptotic_points(...)
8. insert_fitting_points(...)


### 1. plot_equation(...)
* plot_equation(main_window, equation, x_min_inputted, x_max_inputted)
* This is the main function that plots the given equation.
* It simply calls the process_inputs() function and if it succeeds then it plots the equation and returns True.
* Else it returns False indicating unsucessful plotting.
* This function's implementation code is well explained & documented, please delve into the function and read from within it.

### 2. process_inputs(...)
* process_inputs(main_window, equation, x_min_inputted, x_max_inputted)
* This function is called with each sucessful equation plotting attempt
* This function is by far the largest & most complex function in the program
* Most of the computational processing happens in this function, such as :
    - computing the equation's domain 
    - checking if there is intersection between the inputted range and the equation's domain
    - checking if asymptotic points exists in that intersection
    - inserting these asymptotic points and fitting points around them (if any) to smoothen the curve
* Also, Input Sanitization and Error Handling happens in this function rather being placed in a separate function
* This is preferred since they reside in before, in between, and after the processing phase so it would be hard to place them in a separate function
* This function's implementation code is well explained & documented, please delve into the function and read from within it


### 3. update_min_max_coordinates(...)
* update_min_max_coordinates(main_window, x_points_intersection_range, y_points_intersection_range)
* This function is called with each sucessful equation plotting attempt
* It checks if the horizontal/vertical limits of it exceeds the maximum horizontal/vertical limits of all equations plotted and if so it updates them
* This function is essential to adjust the ranges in which the y & x zoom sliders operate within

### 4. compute_domain(...)
* compute_domain(equation)
* This function is called with each sucessful equation plotting attempt
* This function utilizes the sympy library to compute the domain of the equation 
* This function is essential since we must check whether the equation's domain has an intersection with the range that the user inputted in which we can plot the curve in

### 5. compute_intersection(...)
* compute_intersection(x_points_range_sympy, domain)
* This function is called with each sucessful equation plotting attempt
* This function uses the sympy library to compute the intersecion between the provided x range and the domain of the function
* First it computes the Intersection and converts it to string then it parses it
* Then it splits it and converts it to a List so that it can be processed more easily in the other functions


### 6. compute_asymptotic_points(...)
* compute_asymptotic_points(intersection)
* This function is called with each sucessful equation plotting attempt
* This Function assumes that the parsed intersection is valid and contains at least two elements (else it returns an empty list anyways)
* This Function assumes that asymptotic point is a point whose curve approaches an infinite vertical line at its location "from both sides" (such as in 1/(x-2))
* This Function doesn't consider points whose curve approaches an infinite vertical line at it location  "from a single side" to be an asymptotic point (such as log10(x))
* The algorithm used by the function to find Asymptotic points is as follows (assume intersection holds [-100, 2, 2, 5, 5, 100]): 
    1. Pop the first and last points from the intersection, where these points represent the limits of the intersection (thus intersection will be = [2, 2, 5, 5])
    2. Remove any duplicates present by converting intersection to set then to list again (thus intersection will be [2, 5])
    3. Assign parsed_intersectoin to asymptotic_points
    4. Sort asymptotic_points (because python set isn't sorted by default) then finally return it


### 7. insert_asymptotic_points(...)
* insert_asymptotic_points(asymptotic_points, x_points_intersection_range, y_points_intersection_range)
* This function is called with each sucessful equation plotting attempt.
* This function inserts nan for each asymptotic point of the equation.
* This is required to avoid undesired connections between the minimum and maximum points around the asymptotic point.
* This Function uses an efficient binary search algorithm to search whether the asymptotic points are already inserted and if so it does nothing (since that means they've been inserted earlier with either inf or nan), else it inserts them.
* This function inserts into sorted lists while preserving them being sorted, that's why binary search is used.
* The Complexity of this function is m\*nlog(n) where:
    - m = number of asymptotic points
    - n = number of x-point samples (constant determined by the code (roughly around 1e4))
* Therefore assuming n = 1e4, the function will require roughly 1 second of computational time for each 1e3 asymptotic point.

### 8. insert_fitting_points(...)
* insert_fitting_points(asymptotic_points, x_points_intersection_range, y_points_intersection_range, equation_exec)
* This function is called with each sucessful equation plotting attempt.
* This function inserts a group of fitting points around each asymptotic point.
* This is required to improve the curve smoothnes at these points and avoid sudden rises and falls around them.
* This Function uses an efficient binary search algorithm to search whether the fitting points are already inserted and if so it does nothing (since that means they've been inserted earlier with their corresponding y values), else it inserts them.
* This function inserts into sorted lists while preserving them being sorted, that's why binary search is used.
* The Complexity of this function is m\*nlog(n) where:
    - m = number of fitting points = 5e1 * number of asymptotic points
    - n = number of x-point samples (constant determined by the code (roughly around 1e4))
* Therefore according to this complexity, the function will require roughly 1 second of computational time for each 1e2 asymptotic point.
* This complexity is by far acceptable, but for plotting equations with large number of asymptotic points it is recommended to go with amore efficient algorithmic approach that has a better time complexity than this one
* It is experimentally found that 6e-1 and 5e1 are appropriate and suitable values that :
    1. Achieve the desired curve smoothnes around the asymptotic points
    2. Achieve an applicable execution time for the function according to its complexity
    3. Do not cause the y-zoom slider to overshoot

<br/>
<!-- }}} -->

<!-- {{{XGrapher Code Documentation (GUI Code)--> 
<br/>

## XGrapher Code Documentation (GUI Code)

The GUI Code of the XGrapher application is simple and straight forward..<br/>
It simply consists of a simple class that represents the main Window of the application.<br/>
This class can be instantiated to create instances of the application's main window.<br/>
The following represents the Documentation the main methods of the class:

1. \_\_init\_\_(...)
2. create_tool_bar(...)
3. create_status_bar(...)
4. create_keypad(...)
5. create_range_fields(...)
6. create_graph(...)
7. create_y_range_slider(...)
8. create_x_range_slider(...)
9. y_range_slider_slot(...)
10. x_range_slider_slot(...)
11. status_bar_print(...)
12. update_legend(...)
13. set_graphical_mode(...)


### 1. \_\_init\_\_(...)
* \_\_init\_\_(self, SCREEN_WIDTH, SCREEN_HEIGHT)
* This method is constructor of the XGrapherWindow class
* This method is responsible for creating the main window of the application and setting its dimensions relative to the screen resolution
* By default, this method will set the graphical mode to light
* All OS specific operations are handled by the os python module to ensure the application achieves cross-platform experience

### 2. create_tool_bar(...)
* create_tool_bar(self)
* This method is repsonsible for creating the Tool Bar

### 3. create_status_bar(...)
* create_status_bar(self)
* This method is repsonsible for creating the Status Bar

### 4. create_keypad(...)
* create_keypad(self)
* This method is repsonsible for creating the Keypad and the Equation's Input Field

### 5. create_range_fields(...)
* create_range_fields(self)
* This method is repsonsible for creating the Input Field for the minimum and maximum x values

### 6. create_graph(...)
* create_graph(self)
* This method is repsonsible for creating the graph in which we will plot into

### 7. create_y_zoom_slider(...)
* create_y_zoom_slider(self)
* This method is responsible for creating the y-zoom slider and connecting its signal to its appropriate slot

### 8. create_x_zoom_slider(...)
* create_x_zoom_slider(self)
* This method is responsible for creating the x-zoom slider and connecting its signal to its appropriate slot

### 9. y_zoom_slider_slot(...)
* y_zoom_slider_slot(self)
* This method represents the slot connected to the signal fired by the y-zoom slider 
* It is responsible for stretching in and out the Y-Axis for achieving an enhanced view and better user experience overall
* The algorithm of the slot is that it centers the plot according to the minimum and maximum y points among all the curves in the plot 
* Then the y-zoom slider stretches and shrinks the y-axis accordingly
* The minimum and maximum y points are being continuously updated by the update_min_max_coordinates() function each time a curve gets plotted

### 10. x_zoom_slider_slot(...)
* x_zoom_slider_slot(self)
* This method represents the slot connected to the signal fired by the x-zoom slider 
* It is responsible for stretching in and out the X-Axis for achieving an enhanced view and better user experience overall
* The algorithm of the slot is that it centers the plot according to the minimum and maximum x points among all the curves in the plot 
* Then the x-zoom slider stretches and shrinks the x-axis accordingly
* The minimum and maximum x points are being continuously updated by the update_min_max_coordinates() function each time a curve gets plotted

### 11. status_bar_print(...)
* status_bar_print(self, message, status)
* This function is responsible for dynamically updating the status bar with the appropriate message and status color
* The if else implementation for this function is preferred over python's switch statement for the sake of backward compatibility
    - status == 0 : indicates Success
    - status < 0  : indicates Error
    - status > 0  : indicates Warning

### 12. update_legend(...)
* update_legend(self)
* This function updates the legend, which is the area at the top left that displays the functions that are plotted

### 13. set_graphical_mode(...)
* set_graphical_mode(self, graphical_mode)
* This function is responsible for changing the graphical mode of the application
    - graphical_mode >  0   :   light mode
    - graphical_mode <= 0   :   dark mode



<br/>
<!-- }}} -->





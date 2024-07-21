
# It is preferred to have a separate file for the imports 
# since as the project grows and uses more libraries and frameworks, the
# imports will bloat the file which might be a bit annoying for the developers
from _XGRAPHER_LOGIC_IMPORTS_ import *



# This is the main function that plots the given equation
# It simply calls the process_inputs() function and if it succeeds then it plots the equation and returns True
# Else it returns False indicating unsucessful plotting
# This function's implementation code is well explained & documented, please delve into the function and read from within it
def plot_equation(main_window, equation, x_min_inputted, x_max_inputted):

    # equation_str represents the equation after:
    #   1. ensuring it has no ** (since this represents the exponentiation operator in python)
    #   2. removing any space character present
    # this step fixes some syntax errors done by the user and causes some misconceptions to him/her
    # fixed syntax errors : if the user entered "5 .2*x" it will get interpreted as 5.2*x
    # misconceptions to the user : if the user entered "5 .2*x" he/she might think it will get interpreted as 5*0.2*x
    equation_str = ''.join(equation.split()) 

    # Here the inputs are being processed and the processing_state is being returned
    # this processing_state will either be:
    # - True in case of sucessful processing 
    # - False in case of unsucessful processing 
    # x_points_intersection_range & y_points_intersection_range represent the x & y points in the intersection 
    # range between the inputted range and the domain of the function respectively (if any)
    processing_state, x_points_intersection_range, y_points_intersection_range = process_inputs(main_window, equation, x_min_inputted, x_max_inputted)
    
    # if unsucessful processing, return False indicating unsucessful plotting of the equation
    # else plot the equation and return True indicating sucessful plotting of the equation
    if (processing_state != True) :
        return False
    else :
        # Here the curve is plotted after all the sanitization and processing done
        main_window.graph.plot(x_points_intersection_range, y_points_intersection_range, label="y = "+equation_str)
         
        # Here the legend is being updated to display the label of the new function
        main_window.update_legend()

        # Here the graph is updated to display the new curve and its legend
        main_window.canvas.draw()

        return True

    return True
 


# This function is called with each sucessful equation plotting attempt
# This function is by far the largest & most complex function in the program
# Most of the computational processing happens in this function, such as :
# - computing the equation's domain 
# - checking if there is intersection between the inputted range and the equation's domain
# - checking if asymptotic points exists in that intersection
# - inserting these asymptotic points and fitting points around them (if any) to smoothen the curve
# Also, Input Sanitization and Error Handling happens in this function rather being placed in a separate function
# This is preferred since they reside in before, in between, and after the processing phase so it would be hard to place them in a separate function
# This function's implementation code is well explained & documented, please delve into the function and read from within it
def process_inputs(main_window, equation, x_min_inputted, x_max_inputted):

    # '**' is considered syntax error, user must use '^' for exponentiation
    if (equation.find('**') > -1):
        main_window.status_bar_print("Syntax Error! Please make sure you entered the equation properly and try again...", -1)
        return [False, [], []]

    # This code block checks if x_min_inputted and x_max_inputted are real numbers that can be processed
    # It does so by attempting to convert the input to float and checks whether the operation is sucessful or not
    try:
        x_min_inputted = float(x_min_inputted)
        x_max_inputted = float(x_max_inputted)
    except :
        main_window.status_bar_print("Error! The provided range is invalid, please enter an appropriate range and try again...", -1)
        return [False, [], []]

    # This code block checks if the input range is reversed or there is nor range at all (i.e. user entered the same point twice)
    if (x_min_inputted>=x_max_inputted):
        main_window.status_bar_print("Error! The provided range is invalid, please enter an appropriate range and try again...", -1)
        return [False, [], []]


    # equation_str represents the equation after:
    #   1. ensuring it has no ** (since this represents the exponentiation operator in python)
    #   2. removing any space character present
    # this step fixes some syntax errors done by the user and causes some misconceptions to him/her
    # fixed syntax errors : if the user entered "5 .2*x" it will get interpreted as 5.2*x
    # misconceptions to the user : if the user entered "5 .2*x" he/she might think it will get interpreted as 5*0.2*x
    equation_str = ''.join(equation.split()) 


    # Here an assumption is made that the inputted equation is a single real number that represents a horizontal line
    # First, the equation_str is converted to float() and if an error encountered it raises a ValueError, and in this case it is simply passed to continue the rest of the code
    # else if no error encountered, we check if the user entered a very big number that is interpreted as inf by matplotlib and thus it isn't able to graph it, 
    # and if so then a FloatingPointError/OverflowError is raised and in this case the code returns False
    # else we update the minimum/maximum y and x points so that the zoom sliders are updated with the latest curves in the graph and adjusts their range accordingly
    # the +-10 in the list that represent the y_range is for the sake of some tolerance that the y-zoom slider can work in
    # Then the horizontal line is plotted and the user is informed about the success of the operation and the code returns
    try: 
        horizontal_line_dy = float(equation_str)
        if ((x_min_inputted == numpy.inf) or (x_max_inputted == numpy.inf)):
            raise OverflowError
        update_min_max_coordinates(main_window, [x_min_inputted, x_max_inputted], [horizontal_line_dy-10, horizontal_line_dy+10])
    except ValueError:
        pass
    except (FloatingPointError, OverflowError):
        main_window.status_bar_print("Error! Please Ensure that the equation doesn't cause overflow within the specified range...", -1)
        return [False, [], []]
    else:
        main_window.status_bar_print("Successfully plotted the equation!", 0)
        return [True, numpy.array([x_min_inputted, x_max_inputted]), [horizontal_line_dy, horizontal_line_dy]]


    # equation_exec represents the equation parsed and ready to be executed using the eval() function. 
    equation_exec = equation_str.replace('^', '**') 
    equation_exec = equation_exec.replace('sqrt', 'numpy.sqrt') 
    equation_exec = equation_exec.replace('log10', 'numpy.log10') 

    # equation_sympy represents the equation parsed and ready to be processed by Sympy library.
    equation_sympy = equation_str.replace('^', '**')
    equation_sympy = equation_sympy.replace('log10', 'log') 
     
    # x_points_range_sympy represents the range of x points in a form which can be processed by Sympy library.
    x_points_range_sympy = 'Interval({}, {})'.format(x_min_inputted, x_max_inputted)

    try:
        # equation_domain represents the domain of the equation
        equation_domain = compute_domain(equation_sympy)

        # intersection represents a parsed and ready to be processed version of the intersection between the inputted x range and equation's domain 
        intersection = compute_intersection(x_points_range_sympy, equation_domain)
         
        # if the intersection list length is less than 2, that means there is no intersection between the inputted x range and the equation's domain
        # in this case we notify the user and return without plotting the equation 
        # else, we check if the equation contains any asymptotic points over the range of intersection and store them in the list asymptotic_points
        if (len(intersection) < 2):
            main_window.status_bar_print("Warning, no intersection exists between the specified range and the equation's domain", 1)
            return [False, [], []]
        else:
            asymptotic_points = compute_asymptotic_points(intersection)

        # Here a list of 1e4 x points equally divided over the intersection range is generated
        # It is experimentally found that 1e4 x points is an appropriate amount which is suitable for both the smoothness of the curve and the complexity of the statement (i.e. execution time is acceptable)
        # numpy.linspace() is used since all elements in x_range_applicable should be floats to avoid issues with some mathematical operators and functions
        # for an instance, in order to raise to a -ve power using Python's built-in Exponentation Operator '**', then at least one of the operands should be float
        # Also, numpy.linspace() holds elements of type numpy.float64 and this is preferred since its division by 0 can be ignored and inf is returned, unlike
        # the regular python float whose division by zero can't be ignored and raises an exception which abandons the creation of x_range_applicable in the middle
        x_min_applicable = float(intersection[0])
        x_max_applicable = float(intersection[-1])
        x_points_intersection_range = numpy.linspace(x_min_applicable, x_max_applicable, 10000)

        # Here a list of x-point-correspondant y-points are being generated over the intersection range using the provided equation
        # Errors such as divide by 0 or sqrt(-ve) or log(0 or -ve) are being ignored and the points which resulted in these types 
        # of errors will either hold inf or nan respectively (this is essential so that matplotlib doesn't connect the points at the sides of an asymptote)
        # Any Syntax Error will cause an exception and will be catched, then the user will be informed about it
        # Any Syntax/Overflow/Name Error will cause an exception and will be catched, then the user will be informed accordingly and the function will return
        # for an instance :
        # equation_exec = hello causes Name Error 
        # equation_exec = 1x2 causes Syntax Error
        # equation_exec = 12.2.4 causes Syntax Error
        # equation_exec = x**9999999 causes FloatingPointError/Overflow Error
        # equation_exec = x**2 but range is [-1e900, 1e900] FloatingPointError/Overflow Error
        with numpy.errstate(divide='ignore', invalid='ignore'):
            y_points_intersection_range = [eval(equation_exec) for x in x_points_intersection_range]

        # Here x_points_intersection_range is converted to a regular python list due to its flexibility and ease of use with 
        # functions compared to numpy's numpy.ndarray type
        x_points_intersection_range = [float(i) for i in numpy.array(x_points_intersection_range)]

        # Here the function inserts the asymptotic points into the x points and nan into the corresponding 
        # y points (if they aren't already inserted) so that matplotlib doesn't connect the points at the sides of an asymptote  
        insert_asymptotic_points(asymptotic_points, x_points_intersection_range, y_points_intersection_range)

        # Here the function inserts fitting points around the asymptotic points so that the curve looks as natural & smooth as 
        # possible without undesired connections between two adjacent points with large difference in their y-coordinates
        insert_fitting_points(asymptotic_points, x_points_intersection_range, y_points_intersection_range, equation_exec)
         
        # Here maximum and minimum x and y among the points of all curves in the graph is being updated  
        update_min_max_coordinates(main_window, x_points_intersection_range, y_points_intersection_range)

        # Here the x_points_intersection_range is converted back to numpy.ndarray() because matplotlib plot() function obliges so
        x_points_intersection_range = numpy.array(x_points_intersection_range)

    except (SyntaxError, NameError):
        # Any SyntaxError/NameError in the equation the user provided will be caught and he/she will be informed
        main_window.status_bar_print("Syntax Error! Please make sure you entered the equation properly and try again...", -1)
        return [False, [], []]
    except (FloatingPointError, OverflowError):
        # Any FloatingPointError/OverflowError in the equation the user provided will be caught and he/she will be informed
        main_window.status_bar_print("Error! Please Ensure that the equation doesn't cause overflow within the specified range...", -1)
        return [False, [], []]
    else:
        # If no exceptions encountered, that means the equation was plotted successfully
        main_window.status_bar_print("Successfully plotted the equation!", 0)
        return [True, x_points_intersection_range, y_points_intersection_range]

    return [True, x_points_intersection_range, y_points_intersection_range]


# This function is called with each sucessful equation plotting attempt
# It checks if the horizontal/vertical limits of it exceeds the maximum
# horizontal/vertical limits of all equations plotted and if so it updates them
# This function is essential to adjust the ranges in which the y & x zoom sliders operate within
def update_min_max_coordinates(main_window, x_points_intersection_range, y_points_intersection_range):
     
    min_y_in_curve = min(y_points_intersection_range)
    max_y_in_curve = max(y_points_intersection_range)
    min_x_in_curve = min(x_points_intersection_range)
    max_x_in_curve = max(x_points_intersection_range)
    
    # this case happens when the user enters an equation that yields the same value for all x points (for an instance x/x)
    # this case is handled by adding tolerance of +-10 around the horizontal line plotted so that the slider can operate in
    # this case happens for y only and not for x, since the user isn't allowed to enter the same value for x_min and 
    # x_max and if he did so this error will be handled in plot_equation() function
    if (min_y_in_curve, max_y_in_curve):
        min_y_in_curve = min_y_in_curve-10
        max_y_in_curve = max_y_in_curve+10

    curve_y_range = max_y_in_curve-min_y_in_curve
    curve_x_range = max_x_in_curve-min_x_in_curve
    
    # The numpy.inf condition is essential to be able to zoom in curves with asymptotic points, because these points 
    # will have y value = +- inf thus y-zoom slider will cause an error when trying to compute the range it should zoom to
    if ((min_y_in_curve < main_window.min_y_in_graph) and (min_y_in_curve != -numpy.inf)):
        main_window.min_y_in_graph = min_y_in_curve - (0.1*curve_y_range) # the (0.1*curve_y_range) is for some tolerance

    # The numpy.inf condition is essential to be able to zoom in curves with asymptotic points, because these points 
    # will have y value = +- inf thus y-zoom slider will cause an error when trying to compute the range it should zoom to
    if ((max_y_in_curve > main_window.max_y_in_graph) and (max_y_in_curve != numpy.inf)):
        main_window.max_y_in_graph = max_y_in_curve + (0.1*curve_y_range) # the (0.1*curve_y_range) is for some tolerance

    if (min_x_in_curve < main_window.min_x_in_graph):
        main_window.min_x_in_graph = min_x_in_curve - (0.1*curve_x_range) # the (0.1*curve_x_range) is for some tolerance

    if (max_x_in_curve > main_window.max_x_in_graph):
        main_window.max_x_in_graph = max_x_in_curve + (0.1*curve_x_range) # the (0.1*curve_x_range) is for some tolerance


        


# This function is called with each sucessful equation plotting attempt
# This function utilizes the sympy library to compute the domain of the equation 
# This function is essential since we must check whether the equation's domain has 
# an intersection with the range that the user inputted in which we can plot the curve in
def compute_domain(equation):
    var('x')
    equation = eval(equation)
    continuous_domain(equation, x, S.Reals)
    domain = continuous_domain(equation, x, S.Reals)
    domain = str(domain)
    return domain

# This function is called with each sucessful equation plotting attempt
# This function uses the sympy library to compute the intersecion between the provided x range and the domain of the function
# First it computes the Intersection and converts it to string then it parses it
# Then it splits it and converts it to a List so that it can be processed more easily in the other functions
def compute_intersection(x_points_range_sympy, domain):
    intersection = str(Intersection(x_points_range_sympy, domain))
    replacements = {
        'Interval'  : '', 
        'Union'     : '', 
        '.open'     : '', 
        '.Ropen'    : '', 
        '.Lopen'    : '', 
        ','         : '', 
        '('         : '', 
        ')'         : '', 
        '{'         : '',
        '}'         : ''
    }
    for old, new in replacements.items():
        intersection = intersection.replace(old, new)
    intersection = intersection.split(' ')
    if (len(intersection) > 1) :
        intersection = [float(n) for n in intersection]
    return intersection

# This function is called with each sucessful equation plotting attempt
# This Function assumes that the parsed intersection is valid and contains at least two elements (else it returns an empty list anyways)
# This Function assumes that asymptotic point is a point whose curve approaches an infinite vertical line at its location *from both sides* (such as in 1/(x-2))
# This Function doesn't consider points whose curve approaches an infinite vertical line at it location  *from a single side* to be an asymptotic point (such as log10(x))
# The algorithm used by the function to find Asymptotic points is as follows (assume intersection holds [-100, 2, 2, 5, 5, 100]): 
# 1. pop the first and last points from the intersection, where these points represent the limits of the intersection (thus intersection will be = [2, 2, 5, 5])
# 2. remove any duplicates present by converting intersection to set then to list again (thus intersection will be [2, 5])
# 3. assign parsed_intersectoin to asymptotic_points
# 4. sort asymptotic_points (because python set isn't sorted by default) then finally return it
def compute_asymptotic_points(intersection):
    if (len(intersection) < 2):
        return []
    else:
        intersection_copy = intersection.copy()
        intersection_copy.pop(0)
        intersection_copy.pop(-1)
        assymptotic_points = list(set(intersection_copy))
        assymptotic_points.sort()
    return assymptotic_points

# This function is called with each sucessful equation plotting attempt.
# This function inserts nan for each asymptotic point of the equation.
# This is required to avoid undesired connections between the minimum and maximum points around the asymptotic point.
# This Function uses an efficient binary search algorithm to search whether the asymptotic points are already 
# inserted and if so it does nothing (since that means they've been inserted earlier with either inf or nan), else it inserts them.
# This function inserts into sorted lists while preserving them being sorted, that's why binary search is used.
# The Complexity of this function is m*nlog(n) where:
#   - m = number of asymptotic points
#   - n = number of x-point samples (constant determined by the code (roughly around 1e4))
# Therefore assuming n = 1e4, the function will require roughly 1 second of computational time for each 1e3 asymptotic point.
def insert_asymptotic_points(asymptotic_points, x_points_intersection_range, y_points_intersection_range):

    for point in asymptotic_points:
        point = float(point)
        low = 0
        high = len(x_points_intersection_range)
        while low < high:
            mid = (low+high)//2
            if x_points_intersection_range[mid] < point:
                low = mid+1
            else: 
                high = mid
        if low == len(x_points_intersection_range) or x_points_intersection_range[low] != point:
            x_points_intersection_range.insert(low, point)
            y_points_intersection_range.insert(low, numpy.nan)

# This function is called with each sucessful equation plotting attempt.
# This function inserts a group of fitting points around each asymptotic point.
# This is required to improve the curve smoothnes at these points and avoid sudden rises and falls around them.
# This Function uses an efficient binary search algorithm to search whether the fitting points are already 
# inserted and if so it does nothing (since that means they've been inserted earlier with their corresponding y values), else it inserts them.
# This function inserts into sorted lists while preserving them being sorted, that's why binary search is used.
# The Complexity of this function is m*nlog(n) where:
#   - m = number of fitting points = 5e1 * number of asymptotic points
#   - n = number of x-point samples (constant determined by the code (roughly around 1e4))
# Therefore according to this complexity, the function will require roughly 1 second of computational time for each 1e2 asymptotic point.
# It is experimentally found that 6e-1 and 5e1 are appropriate and suitable values that :
# 1. Achieve the desired curve smoothnes around the asymptotic points
# 2. Achieve an applicable execution time for the function according to its complexity
# 3. Do not cause the y-zoom slider to overshoot
def insert_fitting_points(asymptotic_points, x_points_intersection_range, y_points_intersection_range, equation_exec):

    fitting_points = []
    for point in asymptotic_points:
        fitting_range = [float(i) for i in numpy.linspace(point+6e-1, point-6e-1, 50)]
        fitting_points = fitting_points+fitting_range 


    for point in fitting_points:
        point = float(point)
        low = 0
        high = len(x_points_intersection_range)
        while low < high:
            mid = (low+high)//2
            if x_points_intersection_range[mid] < point:
                low = mid+1
            else: 
                high = mid
        if low == len(x_points_intersection_range) or x_points_intersection_range[low] != point:
            x_points_intersection_range.insert(low, point)
            x = point # to substitute in the x present in the equation_exec
            y_points_intersection_range.insert(low, eval(equation_exec))



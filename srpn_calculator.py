from collections import deque
import re

srpn_stack = deque() # main stack for storing the users input

random_number_index = -1 # used to store the index of the random number that will be pushed onto the stack

# tuple of all "random" numbers in the calculator
RANDOM_NUMBERS = (
    1804289383, 846930886, 1681692777, 1714636915, 1957747793, 424238335, 719885386, 1649760492,
    596516649, 1189641421, 1025202362, 1350490027, 783368690, 1102520059, 2044897763, 1967513926,
    1365180540, 1540383426, 304089172, 1303455736, 35005211, 521595368
)

# used for cheking saturation
MAX_NUMBER = 2147483647
MIN_NUMBER = -2147483648


"""
stack functions
"""
def push(element):
    if check_overflow():
        print("Stack overflow.")
    else:
        srpn_stack.append(element)

def pop():
    if check_underflow():
        print("Stack empty.")
    else:
        return srpn_stack.pop()

def peek():
    if check_underflow():
        print("Stack empty.")
    else:
        return srpn_stack[-1]

# if the stack exceeds 22 elements, this is considered full,
# so any elements pushed will be rejected because the stack has overflown
# returns true if the stack is full
def check_overflow():
    return len(srpn_stack) > 22

# if the user tries to access the top element of the stack when the stack is empty,
# the process will be rejected because the stack has underflown
# returns true if the stack has no elements in it
def check_underflow():
    return len(srpn_stack) <= 0

def output_stack():
    for item in srpn_stack:
        print(item)

def push_random_number():
    global random_number_index

    if random_number_index >= 21:
        # if the index has exceeded the length of the array, reset the index
        random_number_index = -1

    random_number_index += 1
    push(RANDOM_NUMBERS[random_number_index])


"""
comment processing
"""
# function splits the input at any indication of a comment
def remove_comments(input_string):
    input_string_no_comments_as_list = re.split("# .*? #|#| ", input_string)
    input_string_no_comments_as_list = list(filter(None, input_string_no_comments_as_list))

    return input_string_no_comments_as_list

def process_comment(input_string):
    # assign the list returned buy splitting the input at a comment or a hash followed by a space or a space
    # this list will contain all strings that are not specified in the regular expression
    input_without_comments = re.split("# .*? #|#", input_string)

    if len(re.findall("# | #", input_string)) % 2 == 0:
        # if the number of hash characters in the string is even, then all comments have been closed,
        # so they can be removed
        input_without_comments = remove_comments(input_string)
    elif len(re.findall("# | #", input_string)) % 2 != 0:
        # if the number of hash characters is odd, then a comment has not been closed, so cannot be removed yet
        comment_ended = False

        while not comment_ended:
            input_string = input()

            comment_ended = (input_string.rfind(" #") != -1) # update the value of the flag

        # once the multi-line comment has been closed,
        # remove the comment and add any non-comment characters to the list of the input
        input_without_comments.extend(remove_comments(input_string))

    list_of_valid_inputs = list(filter(None, input_without_comments))

    # loop through the list of valid inputs in reverse and remove any unrecognised strings
    for element in list_of_valid_inputs[::-1]:
        if len(re.findall("[^-\d+|\d+|[+-\/*%^=]|r|d| ]", element)) > 0:
            list_of_valid_inputs.remove(element)

    # finally, if the list of valid inputs is not empty,
    # format each of the elements of the list so they can be pushed to the stack
    if len(list_of_valid_inputs) > 0:
        for element in list_of_valid_inputs:
            format_input(element)

def comment_started(input_string):
    # returns true if the user has entered "# " (hash followed by a space), indicating that a comment has been started
    return len(re.findall("# ", input_string)) > 0


"""
impute processing
"""
def process_unrecognised_input(unrecognised_input):
    # tell the user their input was not recognised and provide the unrecognised character for reference
    print(f"Unrecognised operator or operand \"{unrecognised_input}\".")

def process_number(number):
    # check for saturation
    if number > MAX_NUMBER:
        push(MAX_NUMBER)
    elif number < MIN_NUMBER:
        push(MIN_NUMBER)
    else:
        # if no saturation is encountered, push the number
        push(number)

def process_operator(operator):
    if operator == "=":
        # output the top element of the stack
        print(peek())
    elif len(srpn_stack) > 1:
        x = pop() # top element
        y = pop() # one below top element

        # perform the desired calculation using the numbers from the top of the stack
        if operator == "+":
            process_number(y + x)
        elif operator == "-":
            process_number(y - x)
        elif operator == "*":
            process_number(y * x)
        elif operator == "/":
            if x == 0:
                # prevent the user from dividing by 0
                print("Divide by 0.")

                # put the numbers back in the stack for further calculations
                process_number(y)
                process_number(x)
            else:
                process_number(y // x)
        elif operator == "%":
            process_number(y % x)
        elif operator == "^":
            if x < 0:
                # prevent the user from raising a number to a negative power
                print("Negative power.")

                # put the numbers back in the stack for further calculations
                process_number(y)
                process_number(x)
            else:
                process_number(y ** x)
        else:
            # if the user has entered an unrecognised character, present an error
            process_unrecognised_input(operator)
    else:
        # inform the user of underflow if they try to perform calculations on a stack with
        # less than two elements
        print("Stack underflow.")

def process_input(formatted_input):
    if len(re.findall("-\d+|\d+", formatted_input)) > 0:
        if formatted_input.startswith("0"):
            # if the user enters an octal number, convert it to decimal and process the decimal
            process_number(int(formatted_input.strip(), 8))
        else:
            process_number(int(formatted_input.strip()))
    elif len(re.findall("[+-\/*%^=]", formatted_input)) > 0:
        process_operator(formatted_input.strip())
    elif formatted_input == "d":
        # if the stack is not empty, output it, otherwise, output -2147483648
        if check_underflow():
            print(MIN_NUMBER)
        else:
            output_stack()
    elif formatted_input == "r":
        push_random_number()
    else:
        process_unrecognised_input(formatted_input)

def format_input(input_string):
    if len(input_string) > 0:
        formatted_input = re.findall("-\d+|\d+|[+-\/*^%]=|[+-\/*^%=]", input_string)
        formatted_input = list(filter(None, formatted_input))

        if len(formatted_input) >= 1:
            for element in formatted_input:
                if len(re.findall("-\d+|\d+|[+-\/*^%]$", element)) > 0:
                    # if the element is a number or ends in an operator other than equals, process the element
                    process_input(element)
                else:
                    # if the operator ends in an equals, and there are other operators before it,
                    # process each in reverse, element starting with the equals
                    for operator in element[::-1]:
                        process_input(operator)
        else:
            process_input(input_string)


"""
main function
"""
def main():
    while True:
        user_input = input()

        # if the user enters "e" to exit the program, break the loop
        if user_input == "e":
            break

        # if the user has started a comment, process the comment, otherwise, format their input
        if comment_started(user_input):
            process_comment(user_input)
        else:
            format_input(user_input)

if __name__ == "__main__":
    main()
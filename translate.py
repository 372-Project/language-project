varDict = {}
functions = {}
function_lines = []
complete_functions = []
java_code = []
hasFunctions = False
global stack
global needsImport
global currentInput

def openFile(filename):
    """Open the specified file and return its contents."""
    try:
        with open(filename, 'r') as file:
            file_contents = file.read()
            return file_contents
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        return None
    except IOError:
        print(f"Error: Unable to open {filename}.")
        return None

def removeComments(contents):
    """Remove comments from the file contents."""
    result = []
    in_comment = False

    for item in contents:
        if (item == "%" or item[0] == "%") and not in_comment:
            in_comment = True
        elif (item == "%" or item[-1] == "%") and in_comment:
            in_comment = False
        elif not in_comment:
            result.append(item)
    return result

def createLines(input):
    """Splits the input text into a list of lines of code."""
    global stack
    result = []
    cur = []
    in_string = False
    in_loop = False
    in_do = False
    in_instead = False
    in_function = False
    is_nested = 0
    string_token = ""
    print("INPUT")
    print(input)
    print()
    for item in input:
        try:
            # Handle functions
            if item == "function":
                in_function = True
                cur.append(item)
            elif in_function:
                if item == "end!":
                    cur.append(item)
                    function_lines.append(cur)
                    cur = []
                    in_function = False
                elif cur[-1] == "using":
                    cur.append(item[:-1])
                else:
                    cur.append(item)
            # Handle strings
            elif item[0] == '"' and not in_string:
                in_string = True
                string_token = item
                # Checking for single words
                if item[-2] == '"':
                    in_string = False
                    print(stack)
                    print(cur)
                    if len(stack) == 0:
                        cur.append(string_token[:-1])
                        result.append(cur)
                        cur = []
                    else:
                        cur.append(string_token)
                    string_token = ""
            elif in_string:
                if item[-2] == '"':
                    in_string = False
                    
                    if len(stack) == 0:
                        string_token += " " + item[:-1]
                        cur.append(string_token)
                        result.append(cur)
                        cur = []
                    else:
                        string_token += " " + item
                        cur.append(string_token)
                    string_token = ""
                else:
                    string_token += " " + item
            # Handle loops, makes it so everything inside is not processed until a later call to createLines
            elif item == "check" and in_loop == False:
                in_loop = True
                stack.append(item)
                print("Added " + item + " to the stack")
                print(stack)
                cur.append(item)
            # Determines if the current depth matches the block
            elif in_loop and len(stack) > 0 and stack[-1] == "check":
                # Handles nesting
                if item in ["given", "check", "instead!"]:
                    if item == "given":
                        in_do = True
                    cur.append(item)
                    stack.append(item)
                    print("Added " + item + " to the stack")
                    print(stack)
                    is_nested += 1
                # Handles either the end of the current block or a nested one
                elif item != "perform!" and item.endswith("!"):
                    # the error is coming from inside this if else block, if there is a
                    # while-if_while block the loop! from the second while will end up in the else
                    # causing the if statement to be ended prematurely.
                    if is_nested > 0 or len(stack) > 1:
                        cur.append(item)
                        print("\n\n")
                        print(item)
                        print("\n\n")
                        print("Popped: " + stack.pop())
                        print(stack)
                        is_nested -= 1
                    else:
                        cur.append(item)
                        result.append(cur)
                        print("Popped: " + stack.pop())
                        print("Last item: " + item)
                        print("Stack size: " + str(len(stack)))
                        print(stack)
                        cur = []
                        in_loop = False
                else:
                    cur.append(item)
            # Handle do blocks, makes it so everything inside is not processed until a later call to createLines
            elif item == "given" and in_do == False:
                in_do = True
                stack.append(item)
                print("Added " + item + " to the stack")
                print(stack)
                cur.append(item)
            # Determines if the current depth matches the block
            elif in_do and len(stack) > 0 and stack[-1] == "given":
                # Handles nesting
                if item in ["given", "check", "instead!"]:
                    cur.append(item)
                    stack.append(item)
                    print("Added " + item + " to the stack")
                    print(stack)
                    is_nested += 1
                # Handles either the end of the current block or a nested one
                elif item != "do!" and item.endswith("!"):
                    if is_nested > 0 or len(stack) > 1:
                        cur.append(item)
                        print("Popped: " + stack.pop())
                        print("Last item: " + item)
                        print(stack)
                        is_nested -= 1
                    else:
                        cur.append(item[:-1])
                        result.append(cur)
                        print("Popped: " + stack.pop())
                        print("Last item: " + item)
                        print(stack)
                        cur = []
                        in_do = False
                else:
                    cur.append(item)
            # Handle instead blocks, makes it so everything inside is not processed until a later call to createLines
            elif item == "instead!" and in_instead == False:
                in_instead = True
                stack.append(item)
                print("Added " + item + " to the stack")
                print(stack)
                cur.append(item)
            # Determines if the current depth matches the block
            elif in_instead and len(stack) > 0 and stack[-1] == "instead!":
                # Handles nesting
                if item in ["given", "check", "instead!"]:
                    cur.append(item)
                    is_nested += 1
                # Handles either the end of the current block or a nested one
                elif item.endswith("!"):
                    if is_nested > 0 or len(stack) > 1:
                        cur.append(item)
                        print("Popped: " + stack.pop())
                        print(stack)
                        is_nested -= 1
                    else:
                        cur.append(item[:-1])
                        result.append(cur)
                        print("Popped: " + stack.pop())
                        print(stack)
                        cur = []
                        in_instead = False
                else:
                    cur.append(item)
            # Handle anything else such as end of line, end of outer loop, etc
            else:
                # Drop the closing of the loop
                if item in ["loop!", "end!"]:
                    pass
                # For the end of regular lines
                elif item.endswith("."):
                    cur.append(item[:-1])
                    result.append(cur)
                    cur = []
                # For the end of do and instead blocks
                elif item.endswith(".!"):
                    cur.append(item[:-2])
                    result.append(cur)
                    cur = []
                else:
                    cur.append(item)
        except:
            raise Exception("Syntax Error for line: "+str(item))

    if cur:
        raise Exception("Error, missing closing expression '.'")
    print("\nRESULT")
    print(result)
    print()
    return result


def startFile(filename):
    """Create a new Java file with the specified filename."""
    global needsImport
    filename_ext = filename + ".java"
    try:
        file = open(filename_ext, 'w')

        if needsImport > 0:
            import_line = "import java.util.Scanner;\n\n"
            java_code.append(import_line)

        class_line = f"public class {filename} {{\n"
        main_line = "\tpublic static void main(String[] args) {\n"
        java_code.append(class_line)
        java_code.append(main_line)

        if needsImport > 0:
            scanner_line = "\t\tScanner in = new Scanner(System.in);\n"
            java_code.append(scanner_line)

        return file
    except (IOError, OSError) as e:
        print(f"Error creating file '{filename}': {e}")
        return None

def endFile(file):
    """Close the Java file and write the end of the main method and class."""
    if needsImport > 0:
        close_line = "\n\t\tin.close();"
        java_code.append(close_line)
    end_main = "\n\t}\n"
    java_code.append(end_main)
    end_class = "}\n"
    java_code.append(end_class)

def typeLines(lines):
    """Assign a line number and line type to each line of code."""
    global needsImport
    line_number = 0
    result = {}
    for line in lines:
        if line[0] == "print":
            result[line_number] = [line, "PRINT"]
        elif line[0] == "given":
            result[line_number] = [line, "CONDITIONAL"]
        elif line[0] == "instead!":
            result[line_number] = [line, "INSTEAD"]
        elif line[0] == "check":
            result[line_number] = [line, "CHECK"]
        elif line[0] == "function":
            result[line_number] = [line, "FUNCTION"]
        elif line[0] == "send":
            result[line_number] = [line, "SEND"]
        elif line[1] == "is":
            if line[2] == "get":
                needsImport += 1
                result[line_number] = [line, "INPUT"]
            elif line[2] == "getnum":
                needsImport += 1
                result[line_number] = [line, "NUMINPUT"]
            elif line[2] == "function!":
                result[line_number] = [line, "CALL"]
            else:
                result[line_number] = [line, "ASSIGNMENT"]
        line_number += 1
    return result

def translate(block_type, source_code_dict, indent):
    """Translate the source code into Java code and write it to the Java file."""
    global currentInput
    global stack
    global varDict
    for line_number, (line, line_type) in source_code_dict.items():
        #print(line)
        if line_type == "ASSIGNMENT":
            variable = line[0]
            expression = translate_expression(line[2:])
            if variable not in varDict.keys():
                var_type = determine_var_type(expression, variable)
                java_line = "\t" * indent + f"{var_type} {variable} = {expression};\n"
            else:
                java_line = "\t" * indent + f"{variable} = {expression};\n"
            if block_type == "regular":
                java_code.append(java_line)
            elif block_type == "function":
                complete_functions.append(java_line)
                
        elif line_type == "PRINT":
            expression = translate_expression(line[1:])
            java_line = "\t" * indent + f"System.out.print({expression});\n"
            if block_type == "regular":
                java_code.append(java_line)
            elif block_type == "function":
                complete_functions.append(java_line)

        elif line_type == "CONDITIONAL":
            expression = translate_expression(line[1:line.index("do!")])
            java_line = "\t" * indent + f"if ({expression}) {{\n"
            if block_type == "regular":
                java_code.append(java_line)
            elif block_type == "function":
                complete_functions.append(java_line)
            rest = createLines(line[line.index("do!") + 1:])
            print(line)
            print("REST")
            print(rest)
            print()
            stack = []
            rest_dict = typeLines(rest)
            print("PLEASE")
            print(rest_dict)
            print()
            translate(block_type, rest_dict, indent + 1)
            java_line = "\t" * indent + "}\n"
            if block_type == "regular":
                java_code.append(java_line)
            elif block_type == "function":
                complete_functions.append(java_line)

        elif line_type == "INSTEAD":
            java_line = "\t" * indent + "else {\n"
            if block_type == "regular":
                java_code.append(java_line)
            elif block_type == "function":
                complete_functions.append(java_line)
            rest = createLines(line[1:])
            stack = []
            rest_dict = typeLines(rest)
            translate(block_type, rest_dict, indent + 1)
            java_line = "\t" * indent + "}\n"
            if block_type == "regular":
                java_code.append(java_line)
            elif block_type == "function":
                complete_functions.append(java_line)

        elif line_type == "CHECK":
            expression = translate_expression(line[1:line.index("perform!")])
            java_line = "\t" * indent + f"while ({expression}) {{\n"
            if block_type == "regular":
                java_code.append(java_line)
            elif block_type == "function":
                complete_functions.append(java_line)
            rest = createLines(line[line.index("perform!") + 1:-1])
            stack = []
            rest_dict = typeLines(rest)
            translate(block_type, rest_dict, indent + 1)
            java_line = "\t" * indent + "}\n"
            if block_type == "regular":
                java_code.append(java_line)
            elif block_type == "function":
                complete_functions.append(java_line)

        elif line_type == "INPUT":
            varDict[line[0]] = "String"
            java_line = "\t" * indent + f"String {line[0]} = in.nextLine();\n"
            currentInput += 1
            java_code.append(java_line)

        elif line_type == "FUNCTION":
            if line[3] == "number":
                var_type = "int"
            elif line[3] == "word":
                var_type = "String"
            else:
                var_type = "void"

            if line[5] == "number":
                input = "int input"
            elif line[5] == "word":
                input = "String input"
            else:
                input = ""
            functions[line[1]] = var_type
            temp = indent-1
            java_line = "\t" * temp + "public static " + str(var_type) + " "+ str(line[1]) + "(" + str(input) + "){\n"
            complete_functions.append(java_line)
            rest = createLines(line[6:])
            saveVariable = varDict
            varDict = {}
            stack = []
            rest_dict = typeLines(rest)
            block_type = "function"
            translate(block_type, rest_dict, indent)
            java_line = "\t" * temp + "}\n"
            complete_functions.append(java_line)
            varDict = saveVariable

        elif line_type == "CALL":
            if line[3] not in functions.keys():
                raise Exception("Error, call to function '" + line[3] + "' that does not exist")
            function_type = functions[line[3]]
            java_line = "\t" * indent + function_type + " " + line[0] + " = " + line[3] + "(" + line[4] + ");\n"
            if block_type == "regular":
                java_code.append(java_line)
            elif block_type == "function":
                complete_functions.append(java_line)

        elif line_type == "SEND":
            java_line = "\t" * indent + "return " + line[1] + ";\n"
            complete_functions.append(java_line)

        elif line_type == "NUMINPUT":
            varDict[line[0]] = "int"
            java_line = "\t" * indent + f"String {line[0]}s = in.nextLine();\n"
            currentInput += 1
            if block_type == "regular":
                java_code.append(java_line)
            elif block_type == "function":
                complete_functions.append(java_line)
            java_line = "\t" * indent + f"int {line[0]} = Integer.parseInt({line[0]}s);\n"
            if block_type == "regular":
                java_code.append(java_line)
            elif block_type == "function":
                complete_functions.append(java_line)
        
def determine_var_type(expression, variable):
    """Determine the data type of a variable based on the expression."""
    if expression in varDict.keys():
        varDict[variable] = varDict[expression]
        return varDict[expression]
    elif expression[0] == '"' and expression[-1] == '"':
        varDict[variable] = "String"
        return "String"
    elif expression[0].lower() in ["f", "t"] or expression[0] == '!':
        varDict[variable] = "boolean"
        return "boolean"
    elif expression[0].isdigit():
        varDict[variable] = "int"
        return "int"
    else:
        new_expr = expression.split()[0]
        if new_expr not in varDict or varDict[new_expr] is None:
            raise Exception("Error, variable " + new_expr + " never initialized")
        varDict[variable] = varDict[new_expr]
        return varDict[new_expr]

def translate_expression(tokens):
    """Translate the expression tokens into a Java expression."""
    #print(tokens)
    #print(len(tokens))
    if len(tokens) == 1:
        return translate_value(tokens[0])
    else:
        operator = tokens[0].upper()
        #print(operator)
        operations = {
            "NOT": "!"
        }
        if operator in operations:
            operand = translate_expression(tokens[1:])
            return f"{operations[operator]} {operand}"
        elif len(tokens) >= 3:
            operator = tokens[1].upper()
            left_operand = translate_value(tokens[0])
            right_operand = translate_expression(tokens[2:])
            operations = {
                "ADD": "+", "+": "+",
                "SUB": "-", "-": "-",
                "MULT": "*", "*": "*",
                "DIV": "/", "/": "/",
                "MOD": "%",
                "AND": "&&", "OR": "||",
                "MORETHAN": ">", "LESSTHAN": "<",
                "EQUALS": "==", "NOTEQUALS": "!="
            }
            if operator in operations:
                return f"{left_operand} {operations[operator]} {right_operand}"
            else:
                raise ValueError(f"Invalid operator: {operator}")
        else:
            raise ValueError(f"Invalid expression: {tokens}")

def translate_value(token):
    """Translate the token into a Java value."""
    if token.startswith('"') and token.endswith('"'):
        return token
    elif token.isdigit():
        return token
    elif token in ["T", "F"]:
        return "true" if token == "T" else "false"
    else:
        return token

def main():
    global needsImport
    global currentInput
    global stack
    stack = []
    currentInput = 1
    needsImport = 0
    # input file
    filename = input("Enter the filename (txt extension): ")
    filename_full = filename + ".txt"
    file_contents = openFile(filename_full)
    # read everything and split into words
    contents_list = file_contents.split()
    # remove all comments
    source_code = removeComments(contents_list)
    # create a list of lines
    source_code = createLines(source_code)
    # reset the stack
    stack = []
    # type each line
    source_code_dict = typeLines(source_code)
    java_file = startFile(filename)
    # will now process the lines, if there are any
    if function_lines != None:
            varDict = {}
            complete_functions.append("\n")
            function_dict = typeLines(function_lines)
            translate("functions", function_dict, 2)
            i = 1
            for line in complete_functions:
                java_code.insert(i, line)
                i+=1
    #for key in source_code_dict.keys():
        #print(source_code_dict[key])
    print()
    print(source_code_dict)
    print()
    translate("regular", source_code_dict, 2)
    endFile(java_file)
    java_file.writelines(java_code)
    java_file.close()

if __name__ == "__main__":
    main()

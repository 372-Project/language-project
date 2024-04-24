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
    in_function = False
    string_token = ""
    for item in input:
        try:
            if item == "function":
                hasFunctions = True
                in_function = True
                cur.append(item)
            elif in_function:
                if item == "end!":
                    cur.append(item)
                    function_lines.append(cur)
                    cur = []
                else:
                    cur.append(item)
            # Handle blocks and nesting
            elif item in ["check", "given", "instead!"]:
                stack.append(item)
                cur.append(item)
            # Handle block terminators
            elif item.endswith("!"):
                if len(stack) == 1 and item[:-1] not in ["perform", "do", "instead"]:
                    cur.append(item[:-1])
                    result.append(cur)
                    cur = []
                    stack.pop()
                elif len(stack) > 1 and item[:-1] not in ["perform", "do", "instead"]:
                    cur.append(item)
                    stack.pop()
                elif item == "end!":
                    pass
                else:
                    cur.append(item)
            # Handle end of lines
            elif item.endswith("."):
                if len(stack) == 0:
                    cur.append(item[:-1])
                    result.append(cur)
                    cur = []
                else:
                    cur.append(item)
            else:
                cur.append(item)
        except:
            raise Exception("Syntax Error for line: " + str(item))
    if cur:
        raise Exception("Error, missing closing expression '.'")
    
    if stack:
        raise Exception("Error, unclosed block")
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
    bool_list = {"MORETHAN": ">", "LESSTHAN": "<",
                "EQUALS": "==", "NOTEQUALS": "!="}
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
        elif line[0] == "function!":
            result[line_number] = [line, "CALL"]
        elif line[1] == "is":
            if line[2] == "get":
                needsImport += 1
                result[line_number] = [line, "INPUT"]
            elif line[2] == "getnum":
                needsImport += 1
                result[line_number] = [line, "NUMINPUT"]
            elif line[2] == "function!":
                result[line_number] = [line, "CALL"]
            elif len(line) > 3 and line[3] in bool_list.keys():
                result[line_number] = [line, "BOOLASSIGN"]
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

        elif line_type == "BOOLASSIGN":
            variable = line[0]
            expression = translate_expression(line[2:])
            if variable not in varDict.keys():
                varDict[variable] = "boolean"
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
            stack = []
            rest_dict = typeLines(rest)
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

            if line[5] == "number!":
                input = "int input"
                input_type = "int"
            elif line[5] == "word!":
                input = "String input"
                input_type = "String"
            else:
                input = ""
                input_type = ""
            functions[line[1]] = var_type
            temp = indent-1
            java_line = "\t" * temp + "public static " + str(var_type) + " "+ str(line[1]) + "(" + str(input) + "){\n"
            complete_functions.append(java_line)
            rest = createLines(line[6:])
            saveVariable = varDict
            varDict = {}
            varDict["input"] = input_type
            stack = []
            rest_dict = typeLines(rest)
            block_type = "function"
            translate(block_type, rest_dict, indent)
            java_line = "\t" * temp + "}\n"
            complete_functions.append(java_line)
            varDict = saveVariable

        elif line_type == "CALL":
            # void function call
            if len(line) == 3:
                java_line = "\t" * indent +  line[1] + "(" + line[2] + ");\n"
            else:
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
    if len(tokens) == 1:
        return translate_value(tokens[0])
    else:
        operator = tokens[0].upper()
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
                "ADD": "+", "PLUS": "+", "+": "+",
                "SUB": "-", "MINUS": "-", "-": "-",
                "MULT": "*", "TIMES": "*", "*": "*",
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
    contents_list = []
    in_string = False
    string_token = ""
    skip_char = False
    i = 0
    for char in file_contents:
        if skip_char:
            skip_char = False
            pass
        elif char == '"' and not in_string:
            in_string = True
            string_token = char
        elif in_string:
            string_token += char
            if char == '"':
                in_string = False
                if string_token.endswith('.') or string_token.endswith('.!'):
                    contents_list.append(string_token)
                    string_token = ""
        elif char.isspace() and not in_string:
            if string_token:
                contents_list.append(string_token)
                string_token = ""
        elif char in ['.', '!'] and not in_string:
            string_token += char
            if i < len(file_contents)-1 and file_contents[i+1] == '!':
                string_token += '!'
                skip_char = True
            contents_list.append(string_token)
            string_token = ""
        else:
            string_token += char
        i+=1
    
    if string_token:
        contents_list.append(string_token)
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
    translate("regular", source_code_dict, 2)
    endFile(java_file)
    java_file.writelines(java_code)
    java_file.close()

if __name__ == "__main__":
    main()

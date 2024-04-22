varDict = {}
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
    is_nested = 0
    string_token = ""
    for item in input:
        # Handle strings
        try:
            if item[0] == '"' and not in_string:
                in_string = True
                string_token = item
                # Checking for single words
                if item[-2] == '"':
                    in_string = False
                    cur.append(string_token[:-1])
                    result.append(cur)
                    cur = []
                    string_token = ""
            elif in_string:
                if item[-2] == '"':
                    in_string = False
                    string_token += " " + item[:-1]
                    cur.append(string_token)
                    result.append(cur)
                    cur = []
                    string_token = ""
                else:
                    string_token += " " + item
            # Handle loops, makes it so everything inside is not processed until a later call to createLines
            elif item == "check" and in_loop == False:
                in_loop = True
                stack.append(item)
                cur.append(item)
            # Determines if the current depth matches the block
            elif in_loop and stack[-1] == "check":
                # Handles nesting
                if item in ["given", "check", "instead!"]:
                    if item == "given":
                        in_do = True
                    cur.append(item)
                    stack.append(item)
                    is_nested += 1
                # Handles either the end of the current block or a nested one
                elif item != "perform!" and item.endswith("!"):
                    if is_nested > 0:
                        cur.append(item)
                        stack.pop()
                        is_nested -= 1
                    else:
                        cur.append(item)
                        result.append(cur)
                        cur = []
                        in_loop = False
                else:
                    cur.append(item)
            # Handle do blocks, makes it so everything inside is not processed until a later call to createLines
            elif item == "given" and in_do == False:
                in_do = True
                stack.append(item)
                cur.append(item)
            # Determines if the current depth matches the block
            elif in_do and stack[-1] == "given":
                # Handles nesting
                if item in ["given", "check", "instead!"]:
                    cur.append(item)
                    stack.append(item)
                    is_nested += 1
                # Handles either the end of the current block or a nested one
                elif item != "do!" and item.endswith("!"):
                    if is_nested > 0:
                        cur.append(item)
                        stack.pop()
                        is_nested -= 1
                    else:
                        cur.append(item[:-1])
                        result.append(cur)
                        cur = []
                        in_do = False
                else:
                    cur.append(item)
            # Handle instead blocks, makes it so everything inside is not processed until a later call to createLines
            elif item == "instead!" and in_instead == False:
                in_instead = True
                stack.append(item)
                cur.append(item)
            # Determines if the current depth matches the block
            elif in_instead and stack[-1] == "instead!":
                # Handles nesting
                if item in ["given", "check", "instead!"]:
                    cur.append(item)
                    is_nested += 1
                # Handles either the end of the current block or a nested one
                elif item.endswith("!"):
                    if is_nested > 0:
                        cur.append(item)
                        stack.pop()
                        is_nested -= 1
                    else:
                        cur.append(item[:-1])
                        result.append(cur)
                        cur = []
                        in_instead = False
                else:
                    cur.append(item)
            # Handle anything else such as end of line, end of outer loop, etc
            else:
                # Drop the closing of the loop
                if item == "loop!":
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
    return result


def startFile(filename):
    """Create a new Java file with the specified filename."""
    global needsImport
    filename_ext = filename + ".java"
    try:
        file = open(filename_ext, 'w')

        class_line = f"public class {filename} {{\n"
        main_line = "\tpublic static void main(String[] args) {\n"

        lines = [class_line, main_line]
        if needsImport > 0:
            import_line = "import java.util.Scanner;\n\n"
            file.write(import_line)

        file.writelines(lines)

        if needsImport > 0:
            scanner_line = "\t\tScanner in = new Scanner(System.in);\n"
            file.write(scanner_line)

        return file
    except (IOError, OSError) as e:
        print(f"Error creating file '{filename}': {e}")
        return None

def endFile(file):
    """Close the Java file and write the end of the main method and class."""
    if needsImport > 0:
        close_line = "\n\t\tin.close();"
        file.write(close_line)
    end_main = "\n\t}\n"
    end_class = "}\n"
    lines = [end_main, end_class]
    file.writelines(lines)
    file.close()

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
        elif line[1] == "is":
            if line[2] == "get":
                needsImport += 1
                result[line_number] = [line, "INPUT"]
            elif line[2] == "getnum":
                needsImport += 1
                result[line_number] = [line, "NUMINPUT"]
            else:
                result[line_number] = [line, "ASSIGNMENT"]
        line_number += 1
    return result


def translate(java_file, source_code_dict, indent):
    """Translate the source code into Java code and write it to the Java file."""
    global currentInput
    global stack
    for line_number, (line, line_type) in source_code_dict.items():
        if line_type == "ASSIGNMENT":
            variable = line[0]
            expression = translate_expression(line[2:])
            if variable not in varDict.keys():
                var_type = determine_var_type(expression, variable)
                java_line = "\t" * indent + f"{var_type} {variable} = {expression};\n"
            else:
                java_line = "\t" * indent + f"{variable} = {expression};\n"
            java_file.write(java_line)
        elif line_type == "PRINT":
            expression = translate_expression(line[1:])
            java_line = "\t" * indent + f"System.out.print({expression});\n"
            java_file.write(java_line)
        elif line_type == "CONDITIONAL":
            expression = translate_expression(line[1:line.index("do!")])
            java_line = "\t" * indent + f"if ({expression}) {{\n"
            java_file.write(java_line)
            rest = createLines(line[line.index("do!") + 1:])
            stack = []
            rest_dict = typeLines(rest)
            translate(java_file, rest_dict, indent + 1)
            java_line = "\t" * indent + "}\n"
            java_file.write(java_line)
        elif line_type == "INSTEAD":
            java_line = "\t" * indent + "else {\n"
            java_file.write(java_line)
            rest = createLines(line[1:])
            stack = []
            rest_dict = typeLines(rest)
            translate(java_file, rest_dict, indent + 1)
            java_line = "\t" * indent + "}\n"
            java_file.write(java_line)
        elif line_type == "CHECK":
            expression = translate_expression(line[1:line.index("perform!")])
            java_line = "\t" * indent + f"while ({expression}) {{\n"
            java_file.write(java_line)
            rest = createLines(line[line.index("perform!") + 1:])
            stack = []
            rest_dict = typeLines(rest)
            translate(java_file, rest_dict, indent + 1)
            java_line = "\t" * indent + "}\n"
            java_file.write(java_line)
        elif line_type == "INPUT":
            java_line = "\t" * indent + f"String {line[0]} = in.nextLine();\n"
            currentInput += 1
            java_file.write(java_line)
            varDict[line[0]] = "String"
        elif line_type == "NUMINPUT":

            varDict[line[0]] = "int"        
            java_line = "\t" * indent + f"String {line[0]}s = in.nextLine();\n"
            currentInput += 1
            java_file.write(java_line)
            java_line = "\t" * indent + f"int {line[0]} = Integer.parseInt({line[0]}s);\n"
            java_file.write(java_line)

        
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
            raise Exception("Error, variable never initialized")
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
                "ADD": "+", "+": "+",
                "SUB": "-", "-": "-",
                "MULT": "*", "*": "*",
                "DIV": "/", "/": "/",
                "MOD": "%", "%": "%",
                "AND": "&&", "OR": "||",
                "MORETHAN": ">", "LESSTHAN": "<",
                "EQUALS" : "==", "NOTEQUALS" : "!="
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
    translate(java_file, source_code_dict, 2)
    endFile(java_file)

if __name__ == "__main__":
    main()
varDict = {}
global needsImport
global currentInput

def openFile(filename):
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

# removes comments from file
def removeComments(contents):
    result = []
    inComment = False

    for item in contents:
        if (item == "%" or item[0] == "%") and not inComment:
            inComment = True
        elif (item == "%" or item[-1] == "%") and inComment:
            inComment = False
        elif not inComment:
            result.append(item)
    return result

# turns into lines of code
def createLines(input):
    result = []
    cur = []
    in_string = False
    in_loop = False
    in_do = False
    in_instead = False
    string_token = ""

    for item in input:
        if item[0] == '"' and not in_string:
            in_string = True

            string_token = item  # Remove the opening quotation mark

            if item[-2] == '"':  # Checking for single words
                in_string = False
                cur.append(string_token[:-1])
                result.append(cur)
                cur = []
                string_token = ""

        elif in_string:  # Checking for strings that are more than one word 
            if item[-2] == '"':
                in_string = False
                string_token += " " + item[:-1]  # Remove the closing period
                cur.append(string_token)
                result.append(cur)
                cur = []
                string_token = ""
            else:  #  Happens when there is a word in the middle of a string of words 
                   #  EX: "Hello good world", good would be added here
                string_token += " " + item

        elif item == "perform!":  # Makes it so that what is happening in a loop is not processed until later
            in_loop = True
            cur.append(item)
            
        elif in_loop:
            cur.append(item)
            if item == "loop!":
                result.append(cur)
                cur = []
                in_loop = False

        elif item == "do!":  # Makes it so that what is happening in a do is not processed until later
            in_do = True
            cur.append(item)
            
        elif in_do:
            if item.endswith("!"):
                cur.append(item[:-1])
                result.append(cur)
                cur = []
                in_do = False
            else:
                cur.append(item)

        elif item == "instead!":  # Makes it so that what is happening in an instead is not processed until later
            in_instead = True
            cur.append(item)
            
        elif in_instead:
            if item.endswith("!"):
                cur.append(item[:-1])
                result.append(cur)
                cur = []
                in_instead = False
            else:
                cur.append(item)

        else:
            if item.endswith("."):
                cur.append(item[:-1])  # Remove the period
                result.append(cur)
                cur = []
            elif item == "loop!":
                pass
            else:
                cur.append(item)

    if cur:
        raise Exception("Error, missing closing expression '.'")

    return result


# creates java class with main
def startFile(filename):
    global needsImport
    filename_ext = filename + ".java"
    try:
        file = open(filename_ext, 'w')

        class_line = "public class " + filename + " {\n"
        main_line = "\tpublic static void main(String[] args) {\n"

        lines = [class_line, main_line]
        if needsImport > 0:
            print("import")
            import_line = "import java.util.Scanner;\n\n"
            file.write(import_line)

        file.writelines(lines)

        return file
    except (IOError, OSError) as e:
        print(f"Error creating file '{filename}': {e}")
        return None

# ends the main and class
def endFile(file):
    end_main = "\n\t}\n"
    end_class = "}\n"
    lines = [end_main, end_class]
    file.writelines(lines)
    file.close()

# assigns the line to a line number, and to a line type
def typeLines(lines):
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
            else:
                result[line_number] = [line, "ASSIGNMENT"]
        line_number += 1
    return result

def translate(java_file, source_code_dict, indent):
    global currentInput
    for line_number, (line, line_type) in source_code_dict.items():
        if line_type == "ASSIGNMENT":
            variable = line[0]
            expression = translate_expression(line[2:])
            # around here we need to handle if a NEW variable is being made with at least one other variable
            # need to do type inference so its not labeled NONE
            # EX: var = String + anything else, var is a string
            # EX: var = int + anything besides string, var is an int
            if variable not in varDict.keys():
                var_type = determine_var_type(expression, variable)
                java_line = "\t"*indent + str(var_type) + " " + str(variable) + " = " + str(expression) + ";\n"
            else:
                java_line = "\t"*indent + str(variable) + " = " + str(expression) + ";\n"
            print(java_line)
            java_file.write(java_line)
                            
        elif line_type == "PRINT":
            expression = translate_expression(line[1:])
            java_line = "\t"*indent + "System.out.println(" + str(expression) + ");\n"
            print(java_line)
            java_file.write(java_line)

        elif line_type == "CONDITIONAL":
            expression = translate_expression(line[1:line.index("do!")])
            java_line = "\t"*indent + "if (" + str(expression) + ") {" + "\n"
            print(java_line)
            java_file.write(java_line)
            # call create lines on the rest
            rest = createLines(line[line.index("do!")+1:])
            # make a dict
            dict = typeLines(rest)
            # call translate again
            translate(java_file, dict, indent+1)
            # need to just make a line_type of INSTEAD and a case for it in translate
            java_line = "\t"*indent + "}\n"
            java_file.write(java_line)

        elif line_type == "INSTEAD":
            java_line = "\t"*indent + "else {\n"
            print(java_line)
            java_file.write(java_line)
            # call create lines on the rest
            rest = createLines(line[1:])
            # make a dict
            dict = typeLines(rest)
            # call translate again
            translate(java_file, dict, indent+1)
            # need to just make a line_type of INSTEAD and a case for it in translate
            java_line = "\t"*indent + "}\n"
            java_file.write(java_line)

        elif line_type == "CHECK":
            expression = translate_expression(line[1:line.index("perform!")])
            java_line = "\t"*indent + "while (" + str(expression) + ") {" + "\n"
            print(java_line)
            java_file.write(java_line)
            # call create lines on the rest
            rest = createLines(line[line.index("perform!")+1:])
            # make a dict
            dict = typeLines(rest)
            # call translate again
            translate(java_file, dict, indent+1)
            java_line = "\t"*indent + "}\n"
            java_file.write(java_line)
        
        elif line_type == "INPUT":
            java_line = "\t"*indent + "Scanner in" + str(currentInput) + " = new Scanner(System.in);\n" + "\t"*indent + "String " + str(line[0]) + " = in" + str(currentInput) + ".nextLine();\n"
            currentInput += 1
            print(java_line)
            java_file.write(java_line)
        
def determine_var_type(expression, variable):
    print(expression)
    if expression in varDict.keys():
        varDict[variable] = varDict[expression]
        return varDict[expression]
    elif expression[0] == '"' and expression[-1] == '"':
        varDict[variable] = "String"
        return "String"
    elif expression[0].lower() in ["t", "f"]:
        varDict[variable] = "boolean"
        return "boolean"
    elif expression[0].isdigit():
        varDict[variable] = "int" 
        return "int"
    else:
        newExpr = expression.split()
        newExpr = newExpr[0]
        print(varDict[newExpr])
        varDict[variable] = varDict[newExpr]
        return varDict[newExpr]

def translate_expression(tokens):
    if len(tokens) == 1:
        return translate_value(tokens[0])
    elif len(tokens) >= 3:
        operator = tokens[1]
        left_operand = translate_value(tokens[0])
        right_operand = translate_expression(tokens[2:])
        if operator in ["add", "+"]:
            return f"{left_operand} + {right_operand}"
        elif operator in ["sub", "-"]:
            return f"{left_operand} - {right_operand}"
        elif operator in ["mult", "*"]:
            return f"{left_operand} * {right_operand}"
        elif operator in ["div", "/"]:
            return f"{left_operand} / {right_operand}"
        elif operator in ["mod", "%"]:
            return f"{left_operand} % {right_operand}"
        elif operator in ["AND", "OR"]:
            if operator == "AND":
                return str(left_operand)+ " && " +str(right_operand)
            else:
                return str(left_operand)+ " || " +str(right_operand)
        elif operator in ("moreThan", "lessThan"):
            if operator == "moreThan":
                return str(left_operand)+ " > " +str(right_operand)
            else:
                return str(left_operand)+ " < " +str(right_operand) 
    else:
        raise ValueError(f"Invalid expression: {tokens}")

def translate_value(token):
    if token.startswith("\"") and token.endswith("\""):
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
    # type each line
    source_code_dict = typeLines(source_code)
    java_file = startFile(filename)
    translate(java_file, source_code_dict, 2)
    endFile(java_file)

if __name__ == "__main__":
    main()
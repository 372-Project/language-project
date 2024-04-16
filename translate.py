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
    string_token = ""

    for item in input:
        if item[0] == '"' and not in_string:
            in_string = True

            string_token = item  # Remove the opening quotation mark

            if item[-2] == '"':  # Checking for single words
                in_string = False
                cur.append(string_token[:-1])
                result.append(cur)
                print()
                print(cur)
                print()
                cur = []
                string_token = ""

        elif in_string:  # Checking for strings that are more than one word 
            if item[-2] == '"':
                in_string = False
                string_token += " " + item[:-1]  # Remove the closing period
                cur.append(string_token)
                result.append(cur)
                print()
                print(cur)
                print()
                cur = []
                string_token = ""
            else:  #  Happens when there is a word in the middle of a string of words 
                   #  EX: "Hello good world", good would be added here
                string_token += " " + item
        else:
            if item.endswith("."):
                cur.append(item[:-1])  # Remove the period
                print()
                print(cur)
                print()
                result.append(cur)
                cur = []
            else:
                cur.append(item)

    if cur:
        #result.append(cur)
        raise Exception("Error, missing closing expression '.'")

    return result


# creates java class with main
def startFile(filename):
    filename_ext = filename + ".java"
    try:
        file = open(filename_ext, 'w')

        class_line = "public class " + filename + " {\n"
        main_line = "\tpublic static void main(String[] args) {\n"

        lines = [class_line, main_line]

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
    line_number = 0
    result = {}
    for line in lines:
        if line[1] == "is":
            result[line_number] = [line, "ASSIGNMENT"]
        elif line[0] == "print":
            result[line_number] = [line, "PRINT"]
        elif line[0] == "given":
            result[line_number] = [line, "CONDITIONAL"]
        line_number += 1
    return result

def translate(java_file, source_code_dict):
    print("ENTER TRANSLATE")
    for line_number, (line, line_type) in source_code_dict.items():
        if line_type == "ASSIGNMENT":
            variable = line[0]
            expression = translate_expression(line[2:])
            var_type = determine_var_type(expression)
            java_line = f"\t\t{var_type} {variable} = {expression};\n"
            print(java_line)
            java_file.write(java_line)
        elif line_type == "PRINT":
            expression = translate_expression(line[1:])
            java_line = f"\t\tSystem.out.println({expression});\n"
            print(java_line)
            java_file.write(java_line)
        elif line_type == "CONDITIONAL":
            #expression = processed conditional
            #print("Parsing expression!!!")
            #print(expression)
            #print()
            print("Conditional")
            print(line)
            print()

            expression = translate_expression(line[1:])
            java_line = "\t\tif (" + str(expression) + ") {" + "\n"
            print(java_line)
            java_file.write(java_line)

            # call create lines on the rest
            rest = createLines(line[len(expression)+2:])
            # make a dict
            dict = typeLines(rest)
            # call translate again
            translate(java_file, dict)
            # need to just make a line_type of INSTEAD and a case for it in translate
            java_line = "}\n"
            java_file.write(java_line)

# probably going to become obsolete
def parse_conditional(line):
    result = []
    cur = []
    conditional_expr = False
    string_token = ""
    result.append("if (")
    for item in line:
        # handles nested if statements
        if item == "given":
            result.append(parse_conditional(line[line.index(item):]))
            break
        # handles end of conditional expression
        elif item == "do!":
            # need to process the statement to see if there are multiple strung together
            result.append(cur)
            result.append(") {")
            cur = []
        elif item == "instead!":
            result.append("} else {")
            cur = []
        else:
            if item.endswith(".!"):
                cur.append(item[:-1])
                result.append(cur)
            else:
                cur.append(item)
    result.append("}")
    return result
        
def determine_var_type(expression):
    print("ENTER DETERMINE VAR TYPE")
    if expression[0] == '"' and expression[-1] == '"':
        return "String"
    elif expression[0].lower() in ["t", "f"]:
        return "boolean"
    elif expression[0].isdigit():
        return "int"
    else:
        return "String"

def translate_expression(tokens):
    print("ENTER TRANSLATE EXPRESSION")
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
    print("ENTER TRANSLATE VALUE")
    if token.startswith("\"") and token.endswith("\""):
        return token
    elif token.isdigit():
        return token
    elif token in ["T", "F"]:
        return "true" if token == "T" else "false"
    else:
        return token

def main():
    filename = input("Enter the filename (txt extension): ")
    filename_full = filename + ".txt"
    file_contents = openFile(filename_full)
    contents_list = file_contents.split()
    print("\nChecking contents")
    #for content in contents_list:
    #    print(content)
    #print("Done checking contents\n")
    source_code = removeComments(contents_list)
    #print("AFTER COMMENTS "+ str(source_code))
    #print("\nChecking contents")
    #for item in source_code:
    #    print(item)
    #print("Done checking contents\n")


    source_code = createLines(source_code)

    print("AFTER CREATE LINES "+ str(source_code))
    source_code_dict = typeLines(source_code)
    java_file = startFile(filename)
    translate(java_file, source_code_dict)
    endFile(java_file)

if __name__ == "__main__":
    main()
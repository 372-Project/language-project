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
        if item == "%" and not inComment:
            inComment = True
        elif item == "%" and inComment:
            inComment = False
        elif not inComment:
            result.append(item)
    return result

# turns into lines of code
def createLines(input):
    acc = 0
    result = []
    cur = []
    for item in input:
        
        if item[len(item)-1] == ".":
            cur.append(item[0:-1])
            acc += 1
            result.append(cur)
            cur = []
        else:
            cur.append(item)
    #print("There should be " + str(acc) + " 'lines'")
    return result

# creates java class with main
def startFile(filename):
    filename_ext = filename + ".java"
    try:
        file = open(filename_ext, 'w')

        class_line = "public class " + filename + " {\n"
        main_line = "\tpublic static void main(String[] args) {"

        lines = [class_line, main_line]

        file.writelines(lines)


        return file
    except (IOError, OSError) as e:
        print(f"Error creating file '{filename}': {e}")
        return None

# ends the main and class
def endFile(file):
    end_main = "\n\t}"
    end_class = "\n}"
    lines = [end_main, end_class]
    file.writelines(lines)
    


# assigns the line to a line number, and to a line type
def typeLines(lines):
    line_number = 0
    result = {}
    for line in lines:



        if line[1] == "is":
            result[line_number] = [line, "ASSIGNMENT"]

        # KEVIN: Please change this to how you were thinking -Josh
        elif line[0] == "print":
            result[line_number] = [line, "PRINT"]











        line_number += 1
    return result
            
# just after thinking if we have parenthesis it could pose a challenge but not 
# too concerned rn just trying to get a very basic idea
# also does work with somehting like "val is 7 add 3" will probably require lots of ifs
# if anyone has a better idea please feel free
def translate(file, dict):
    write_lines = []
    for item in dict:

        
        # each typed line entered
        dict_line = dict[item]

        # expression type
        expr = dict_line[1]


        if expr == "ASSIGNMENT":
            i = 0

            # code as list of strings
            code_line = dict_line[0]

            val = code_line[len(code_line)-1]
            name = code_line[0]

            #print("VAL '"+val+"'")


            try :
                int(val)

                to_write = "\n\t\tint " + name + " = " + val + ";"
                write_lines.append(to_write)

            except:
                pass

            # not sure if this try is necessary, i am tired
            try :
                #val_str = str(val)
                if val[0] == "T" or val[0] == "F":
                    to_write = ""
                    if val[0] == "T":
                        to_write = "\n\t\tboolean " + name + " = true;"
                    else:
                        to_write = "\n\t\tboolean " + name + " = false;"
                    write_lines.append(to_write)
                    pass
                elif val[0] == '"':
                    # this is for strings
                    pass
            except:
                pass







        elif expr == "PRINT":
            val = dict_line[0][1]
            to_write = "\n\t\tSystem.out.println("+val+");"
            write_lines.append(to_write)
            
    

    file.writelines(write_lines)








def main():
    filename = input("Enter the filename (txt extension): ")
    filename_full = filename+".txt"
    file_contents = openFile(filename_full)
    
    contents_list = file_contents.split()
    source_code = removeComments(contents_list)

    # at this point, source_code is a list of lines, each line is a list of strings indicating each keyword
    source_code = createLines(source_code)
    #printLinesDebug(source_code)

    # at this point, source_code_dict assigns each line a line number, and a type
    source_code_dict = typeLines(source_code)
    #printDictLinesDebug(source_code_dict)


    # builds file
    java_file = startFile(filename)
    translate(java_file, source_code_dict)
    endFile(java_file)





# DEBUG FUNCTIONS - DELETE LATER
def printLinesDebug(lines):
    print("START OF LINES")
    for line in lines:
        print(line)
    print("END OF LINES\n")

def printDictLinesDebug(lines):
    print("START OF DICTIONARY")
    for line in lines:
        print("LINE #"+str(line) + "==" + str(lines[line]))
        
    print("END OF DICTIONARY\n")
# END DEBUG

main()
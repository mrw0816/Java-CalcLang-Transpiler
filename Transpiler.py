import re


''' get_end_of_expression finds the end of expression by
    searching for the next key word or variable assingment
'''
def get_end_of_expression(expression):
    endChar = len(expression)
    # Check if it contains a space
    if expression.__contains__("msg ") and expression.find("msg ") < endChar:
        endChar = expression.find("msg ")
    if expression.__contains__('msg"') and expression.find('msg"') < endChar:
        endChar = expression.find('msg"')
    if expression.__contains__('show ') and expression.find('show ') < endChar:
        endChar = expression.find('show ')
    if expression.__contains__('newline') and expression.find('newline') < endChar:
        endChar = expression.find('newline')
    if expression.__contains__('newline ') and expression.find('newline ') < endChar:
        endChar = expression.find('newline ')
    if expression.__contains__('input ') and expression.find('input') < endChar:
        endChar = expression.find('input')
    if expression.__contains__('input"') and expression.find('input"') < endChar:
        endChar = expression.find('input"')
    if expression.__contains__('=') and expression.find('=') < endChar:
        expression = expression[:expression.find('=')].strip()
        endChar = expression.rfind(' ')
    return endChar

'''The java file uses a hashmap to store variables so this
    function finds the variables in calcLang and changes the
    variable to varHashMap.get( variableName ) 
    
    Ex:
    calcLang
    x = y + 2
    
    Java
    varHashMap.put( "x" , varHashMap.get( "y" ) + 2 );
'''
def replace_variables(string):

    temp = string
    while True:
        start = re.search('[a-zA-Z]+', temp)
        if start == None:
            break
        else:
            start = start.start()
        end = re.search('[a-zA-Z0-9]+', temp).end()

        var = temp[start: end]
        if not (var == 'cos' or var == 'sin' or var == 'Math' or var == 'sqrt'):
            newVar = 'varHashMap.get( "' + var + '" )'
            string = string.replace(var, newVar)

        temp = temp[temp.find(var) + len(var):]


    return string

#open the file to be converted
with open('test2') as file:
    cl_lines = file.read().splitlines()
    file.close()

java = open('java.txt', 'w')
#Set up java import statements, main method, and scanner
java.write('import java.util.HashMap;\n')
java.write('import java.util.Scanner;\n\n')
java.write('public class CalcLang {\n\n')
java.write('\tpublic static void main(String args[]){\n\n')
java.write('\t\tHashMap<String, Double> varHashMap = new HashMap<>();\n')
java.write('\t\tScanner scnr = new Scanner(System.in);\n\n')
java.write('\t\t//Start of CalcLang code\n')
for line in cl_lines:
    line = line.replace("cos", "Math.cos").replace("sin", "Math.sin").replace("sqrt", "Math.sqrt").replace('--', '').strip()

    while len(line) > 0:
        line = line.strip()
        #print(line)
        if line[0:4] == "msg " or line[0:4] == 'msg"':
            #Write print statement to java file
            java.write('\t\tSystem.out.print("' + line[line.find('"') + 1:line.replace('"', '$', 1).find('"')] + '");\n')
            #Remove whats been written to file from line
            line = line[line.replace('"', '$', 1).find('"')+1:]

        elif line[0:5] == "show ":

            #get the start of the variable name
            expression = line.replace('show', '').strip()

            endChar = get_end_of_expression(expression)
            expression = expression[:endChar]
            line = line[5 + len(expression):]
            expression = replace_variables(expression)

            java.write('\t\tSystem.out.print( ' + expression + ' );\n')

        elif (line[0:7] == "newline" and len(line) == 7) or line[0:8] == "newline ":
            java.write("\t\tSystem.out.println();\n")
            line = line[7:]
        elif line[0:6] == "input " or line[0:6] == 'input"':
            #write system.out for string to file
            java.write('\t\tSystem.out.print("' + line[line.find('"') + 1: line.replace('"',"$", 1).find('"')] + '");\n')
            #get variable name from string
            var = line[line.replace('"', '$', 1).find('"') + 1:].strip()

            #Store the variable using a hashmap<String, Double> in java
            java.write('\t\tvarHashMap.put("' + var\
                       + '", scnr.nextDouble());\n')
            #Remove the transpiled code from line
            line = line[line.replace('"', '$', 1).find('"') + 1:].replace(var, "", 1).strip()

        elif line.__contains__("="):
            #get variable name
            var = line[:line.find("=")]
            expression = line[line.find("=") + 1:]

            #Find the end of expression
            endChar = get_end_of_expression(expression)
            expression = expression[:endChar]

            line = line[line.find(expression) + len(expression):]
            expression = replace_variables(expression)

            var = var.strip()
            java.write('\t\tvarHashMap.put( "' + var + '" , (double)' + expression + " );\n")


java.write('\t}\n}')

java.close()
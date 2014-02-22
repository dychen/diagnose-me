import re

def find_diseases(input_file, output_file):
    for line in input_file:
        if '<name>' in line:
            output_file.write(line.strip().replace('<name>', '').replace('</name>', '') + ": ")
        elif '<desc>' in line:
            output_file.write(line.strip().replace('<desc>', '').replace('</desc>', '') + "\n")

def find_diseases_general(input_file, output_file):
    should_continue = False
    for line in input_file:
        if '<name>' in line and not '.' in line:
            output_file.write(line.strip().replace('<name>', '').replace('</name>', '') + ": ")
            should_continue = True
        elif '<desc>' in line and should_continue is True:
            output_file.write(line.strip().replace('<desc>', '').replace('</desc>', '') + "\n")
            should_continue = False

if __name__ == '__main__':
    input_file = open('ICD10CM_FY2013_Full_XML_Tabular.xml', 'r')
    output_file = open('disease_list.txt', 'w')
    #find_diseases(input_file, output_file)
    find_diseases_general(input_file, output_file)
    input_file.close()
    output_file.close()

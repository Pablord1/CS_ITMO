def myParser():
    from collections import deque
    #Method receives two files, one in YAML format, one in XML format.
    #It returns 2dim dictionary with the content content of each line as a dic
    def parse(yaml):
        


        #dic where each item is a line of the input file in YAML
        lines = yaml.readlines()
        #This will be 2 dimensional array with each line and its content as a dic
        dic = []

        #line is a string with the text of each line
        for line in lines:
            #dic with strings separated by ": "
            parsed_line = line.split(": ")

            '''stripped_parsed_line looks like this:

            ['root:\n']
            ['  day', 'Thurs\n']
            ['  content:\n']
            ['  - practice:\n']
            ['      number', "'1'\n"]
            ['      week', 'even week\n']
            ['      time', '08:20-09:50\n']
            ['      campus', 'Kronverksky pr., d.49, lit.A\n']'''

            #new dic when we clean any left white spaces
            stripped_parsed_line = [i.strip() for i in parsed_line]

            '''stripped_parsed_line looks like this:

            ['root:']
            ['day', 'Thurs']
            ['content:']
            ['- practice:']
            ['number', "'1'"]'''

            #Deletes any unnecessary symbols
            for i in range(len(stripped_parsed_line)):
                stripped_parsed_line[i] = stripped_parsed_line[i].replace(':', '')
                stripped_parsed_line[i] = stripped_parsed_line[i].replace('- ', '')

            '''stripped_parsed_line looks like this:

            ['root']
            ['day', 'Thurs']
            ['content']
            ['practice']
            ['number', "'1'"]
            ['week', 'even week']
            ['time', '0820-0950']
            ['campus', 'Kronverksky pr., d.49, lit.A']
            ['classroom', "'2430'"]'''
            
            #Add the ready line to the dictionary
            dic.append(stripped_parsed_line)
        return dic

    #Method uses recursion to write blocks of info to a file
    queue = deque([]) #This is a list for storing the opened tags
    def convert(x, tab, dic, xml):
        if len(dic[x]) == 1:
            #Opens the tag
            xml.write(tab*"  " + "<" + dic[x][0] + ">\n")
            queue.append(dic[x][0])
            #Recursion
            convert(x+1, tab+1, dic, xml)

        #If the list has field and value
        else:
            try:
                #We use try and except because x+1 can't give IndexError
                if len(dic[x + 1]) != 1:
                    #Prints field and value
                    xml.write(tab * "  " + "<" + dic[x][0] + ">"+ dic[x][1] + "</" + dic[x][0] + ">\n")
                    #Recursion but without updating indexing
                    convert(x+1, tab, dic, xml)
                else:
                    xml.write(tab * "  " + "<" + dic[x][0] + ">"+ dic[x][1] + "</" + dic[x][0] + ">\n")
                    xml.write((tab-1) * "  " + "</" + queue[-1] + ">\n")
                    queue.pop()
                    convert(x+1, tab-1, dic, xml)
            except:
                #This part is for the last line of the dictionary
                xml.write(tab * "  " + "<" + dic[len(dic)-1][0] + ">"+ dic[len(dic)-1][1] + "</" + dic[len(dic)-1][0] + ">\n")
                while len(queue) > 0:
                    xml.write((tab-1) * "  " + "</" + queue[-1] + ">\n")
                    queue.pop()
                    tab -= 1
                return

    #Import the files to work with
    yaml = open("Информатика\Лабы\Лаб 4\inputYAML.yaml", 'r', encoding="utf-8")
    #Open in mode "read" to delete anything that is already in the existing file
    xml = open("Информатика\Лабы\Лаб 4\outputXML.xml", 'w', encoding="utf-8")
    xml = open("Информатика\Лабы\Лаб 4\outputXML.xml", 'a', encoding="utf-8")

    #To obtain a dictionary with tags and values of each line as a 2D array
    dic = parse(yaml)
    tab = 0
    indexes = {3, 12, 21, 30}
    x=0

    xml.write("<?xml version='1.0' encoding='UTF-8'?>\n")
    convert(x, tab, dic, xml)

def parserWithLibs():
    import xmlplain

    # Read the YAML file
    with open("Информатика\Лабы\Лаб 4\inputYAML.yaml") as inf:
        root = xmlplain.obj_from_yaml(inf)

    # Output back XML
    with open("Информатика\Лабы\Лаб 4\outputXMLWithLib.xml", "w") as outf:
        xmlplain.xml_from_obj(root, outf, pretty=True)

#To measure the execution times
import time
start_time = time.time()
myParser()
print("My Parser's time:      --- %s seconds ---" % (time.time() - start_time))

start_time2 = time.time()
parserWithLibs()
print("Parser with libraries: --- %s seconds ---" % (time.time() - start_time2))
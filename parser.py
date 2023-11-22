def myParser():
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
    def convert(x, tab, dic, xml):
        if x == (len(dic)):
            return
        #If the list just has one field
        elif len(dic[x]) == 1:
            #Opens the tag
            xml.write(tab*"  " + "<" + dic[x][0] + ">\n")
            #Recursion
            convert(x+1, tab+1, dic, xml)
            #Closes the tag
            xml.write(tab * "  " + "</" + dic[x][0] + ">\n")
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
            except:
                #This part is for the last line of the dictionary
                xml.write(tab * "  " + "<" + dic[len(dic)-1][0] + ">"+ dic[len(dic)-1][1] + "</" + dic[len(dic)-1][0] + ">\n")
                return

    #Import the files to work with
    yaml = open("Информатика\Лабы\Лаб 4\inputYAML.yaml", 'r', encoding="utf-8")
    #Open in mode "read" to delete anything that is already in the existing file
    xml = open("Информатика\Лабы\Лаб 4\outputXML.xml", 'w', encoding="utf-8")
    xml = open("Информатика\Лабы\Лаб 4\outputXML.xml", 'a', encoding="utf-8")

    #To obtain a dictionary with tags and values of each line as a 2D array
    dic = parse(yaml)
    tab = 2
    indexes = {3, 12, 21, 30}

    xml.write("<?xml version='1.0' encoding='UTF-8'?>\n")
    #To print root
    xml.write("<" + dic[0][0] + ">\n")
    #To print the day
    xml.write("  <" + dic[1][0] + ">"+ dic[1][1] + "</" + dic[1][0] + ">\n")
    for x in indexes:
        #To print "content", since it doesn't follow the same rules
        xml.write("  <" + dic[2][0] + ">\n")
        #Create the block inside "<content>"
        convert(x, tab, dic, xml)
        #To print "content", since it doesn't follow the same rules
        xml.write("  </" + dic[2][0] + ">\n")
    xml.write("</" + dic[0][0] + ">")

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
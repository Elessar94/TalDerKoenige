import pprint
class Parser:
    """
    Parses input to create Projects, ontologies, properties and to link them appropriately
    """
    ##TODO handle empty entries, especially in pretty_lines
    project_data = {}

    def __init__(self, file: str):
        self.file = open(file, 'r')
        self.data=self.prepare_lines()
        self.already_read = list()

    def prepare_lines(self):
        lines = self.file.readlines()
        i = 0;
        while i<len(lines) :
            comment_cut = lines[i].find("//")
            if comment_cut != -1:
                lines[i]=lines[i][0:comment_cut]
                lines[i]= lines[i] + "\n"
            i=i+1
        return lines

    def pretty_line(self, line, to_cut):
        start = line.find(to_cut)
        end = start + len(to_cut)
        new_line = line[0:start] + line[end+1:len(line)]
        while (new_line[0]==' '):
           new_line = new_line[1:len(line)]
        while (new_line[-1]==' ' or new_line[-1]=='\n'):
            new_line = new_line[0:len(new_line)-1]
        return new_line

    def occurences(self,string,char):
        return len(string)-len(string.replace(char,""))

    def find_end(self, start):
        lines = self.data
        if (lines[start].find("{")==-1):
            print("Error, no { in starting line ")
            print(start)
            return -1
        bracketsCount = self.occurences(lines[start],"{")
        i = start + 1
        try:
            while (bracketsCount>0 and i<len(lines)-1):
                bracketsCount = bracketsCount + self.occurences(lines[i],"{")-self.occurences(lines[i],"}")
                i=i+1
        except IndexError:
            print("Ended parsing with open parentheses")
        return i-1

    def read_description(self, start, end):
        description={}
        current_lang= ""
        while start < end:
            if self.data[start].find("Language")!=-1:
                string = self.pretty_line(self.data[start],"Language")
                string = string[0:string.find(",")]
                description[string]={}
                current_lang=string
            if self.data[start].find("Value")!=-1:
                string = self.data[start][self.data[start].find("Value"):len(self.data[start])]
                description[current_lang]= self.pretty_line(string,"Value")
            self.already_read.append(start)
            start = start+1
        return description

    def read_normal_list(self, start, end):
        i = start + 1
        list=[]
        while i < end:
            string = self.pretty_line(self.data[i],"\n")
            if string!="":
               list.append(string)
            self.already_read.append(i)
            i=i+1
        return list

        #TODO maybe write Keywords in ALL CAPS to avoid usage of users.
    def read_ontology(self,start,end):
        ontology_data = {}
        ontology_data["Resources"]=[]
        i = start-1
        while i<end:
            i = i + 1
            if i in self.already_read:
                continue
            line = self.data[i]
            if (line.find("Resource")!=-1):
                ontology_data["Resources"].append(self.read_resource(i,self.find_end(i)))
                continue
            if (line.find("Name")!=-1):
                ontology_data["Name"] = self.pretty_line(line,"Name")
            if (line.find("Label")!=-1):
                ontology_data["Label"] = self.pretty_line(line,"Label")

            self.already_read.append(i)

        return ontology_data

    def read_resource(self,start,end):
        resource_data = {}
        resource_data["Properties"]=[]
        i= start-1
        while i <end:
            i = i + 1
            if i in self.already_read:
                continue
            line = self.data[i]
            if line.find("Property")!=-1:
                resource_data["Properties"].append(self.read_property(i,self.find_end(i)))
                continue

            if line.find("Name")!=-1:
                resource_data["Name"]= self.pretty_line(line, "Name")
            if line.find("Super classes")!=-1:
                resource_data["Super classes"] = self.read_normal_list(i,self.find_end(i))
            if line.find("Labels")!=-1:
                resource_data["Labels"] = self.read_description(i,self.find_end(i))
            if line.find("Comments")!=-1:
                resource_data["Comments"] = self.read_description(i,self.find_end(i))

            self.already_read.append(i)

        return resource_data

    def read_attributes(self,start, end):
        i = start -1
        attributes_data={}

        while i<end:
            i=i+1
            line = self.data[i]
            if i in self.already_read:
                continue
            j = line.find("=")
            if j!=-1:
                one=line[0:j]
                two=line[j+1:len(line)]
                while (one[0]==' '):
                    one = one[1:len(one)]
                while (two[0]==' '):
                    two=two[1:len(two)]
                while (one[-1]==' ' or one[-1]== '\n'):
                    one = one[0:len(one)-1]
                while (two[-1] == ' ' or two[-1] == '\n'):
                    two = two[0:len(two) - 1]
                attributes_data[one]=two
            self.already_read.append(i)
        return attributes_data
    def read_property(self, start, end):
        property_data={}
        i = start-1
        while i <end :
            i = i + 1
            line  = self.data[i]
            if i in self.already_read:
                continue
            if line.find("Name")!=-1:
                property_data["Name"]= self.pretty_line(line, "Name")
            if line.find("Super Properties")!=-1:
                property_data["Super Properties"]=self.read_normal_list(i,self.find_end(i))
            if line.find("Labels")!=-1:
                property_data["Labels"]=self.read_description(i,self.find_end(i))
            if line.find("Object")!=-1:
                property_data["Object"] = self.pretty_line(line, "Object")
            if line.find("Cardinality")!=-1:
                property_data["Cardinality"] = self.pretty_line(line, "Cardinality")
            if line.find("GUI Element")!=-1:
                property_data["GUI Element"] = self.pretty_line(line, "GUI Element")
            if line.find("GUI Attributes")!=-1:
                property_data["GUI Attributes"]= self.read_attributes(i,self.find_end(i))
            self.already_read.append(i)
        return property_data

    def read_project(self):
        lines = self.data
        i = -1
        while i<len(self.data)-1 :
            i = i + 1
            if i in self.already_read:
                continue
            line = self.data[i]
            if line.find("Ontology")!=-1:
                self.project_data["Ontology"] = self.read_ontology(lines.index(line),self.find_end(lines.index(line)))
                continue
            if (line.find("Short code")!=-1):
                self.project_data["Short code"] = self.pretty_line(line,"Short code")
            if (line.find("Short name") != -1):
                self.project_data["Short name"] = self.pretty_line(line,"Short name")
            if (line.find("Long name") != -1):
                self.project_data["Long name"] = self.pretty_line(line, "Long name")
            if (line.find("Description") != -1):
                self.project_data["Description"]=self.read_description(lines.index(line),self.find_end(lines.index(line)))
            if line.find("Keywords")!=-1:
                self.project_data["Keywords"] = self.read_normal_list(lines.index(line),self.find_end(lines.index(line)))
            if line.find("Logo")!=-1:
                self.project_data["Logo"] = self.read_normal_list(lines.index(line),self.find_end(lines.index(line)))

            self.already_read.append(i)

        return self.project_data


parser = Parser("ubkvp-onto")
pprint.pprint(parser.read_project())

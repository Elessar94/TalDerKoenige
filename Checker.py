import sys
from typing import List, Set, Dict, Tuple, Optional
import pprint
from Parser import Parser

#TODO include Lists
class Checker:

    def __init__(self, dict):
        self.dict = dict
        self.can_continue = True

    def check_project(self):
        necessary_keys = ["Ontology", "Short code", "Short name", "Long name"]
        possible_keys = ["Description", "Keywords", "Logo"]
        for key in necessary_keys:
            if not key in self.dict:
                self.can_continue = False
                print ("The following key is necessary and is missing: ")
                print(key)

        for key in possible_keys:
            if not key in self.dict:
                self.dict[key] = None

        for key in self.dict:
            if not key in possible_keys and not key in necessary_keys:
                print("The following key was used but was not recognized: ")
                print(key)
        return

    def check_onto(self):
        necessary_keys = ["Name"]
        possible_keys = ["Label", "Resources"]
        for key in necessary_keys :
            if not key in self.dict["Ontology"]:
                self.can_continue = False
                print("The following key is necessary for the ontology and is missing: ")
                print(key)

        for key in possible_keys:
            if not key in self.dict["Ontology"]:
                self.dict["Ontology"][key] = None

        for key in self.dict["Ontology"]:
            if not key in possible_keys and not key in necessary_keys:
                print("The following key was used in the ontology but was not recognized: ")
                print(key)
        return

    def check_res(self):
        necessary_keys = ["Name"]
        possible_keys = ["Properties", "Labels", "Comments", "Super classes"]
        for resource in self.dict["Ontology"]["Resources"]:
            for key in necessary_keys:
                if not key in resource:
                    self.can_continue = False
                    print("In the resource ")
                    #pprint.pprint(resource)
                    print("The following key is necessary and missing: ")
                    print(key)

            for key in possible_keys:
                if not key in resource:
                    resource[key] = None

            for key in resource:
                if not key in possible_keys and not key in necessary_keys:
                    print("In the resource")
                    #pprint.pprint(resource)
                    print("The following key was used but was not recognized: ")
                    print(key)
        return

    def check_prop(self):
        necessary_keys = ["Name", "Super Properties", "Object", "Cardinality","GUI Element"]
        possible_keys = ["Labels", "GUI Attributes"]
        for resource in self.dict["Ontology"]["Resources"]:
                for property in resource["Properties"]:
                    for key in necessary_keys:
                        if not key in property:
                            self.can_continue = False
                            print("In the resource ")
                            pprint.pprint(resource["Name"]) #catch error if name is the missing key
                            print("In the property ")
                            pprint.pprint(property["Name"]) #same as above
                            print("The following key is necessary and missing: ")
                            print(key)

                    for key in possible_keys:
                        if not key in property:
                            property[key] = None

                    for key in property:
                        if not key in possible_keys and not key in necessary_keys:
                            print("In the resource")
                            #pprint.pprint(resource)
                            print("In the property")
                            #pprint.pprint(property)
                            print("The following key was used but was not recognized: ")
                            print(key)
        return


    def check(self):
        self.check_project()
        self.check_onto()
        self.check_res()
        self.check_prop()
        if not self.can_continue:
            print("Errors are fatal, can not create project. Please revise and try again.")
            sys.exit()
        return self.dict

parser = Parser("ubkvp-onto")
checker = Checker(parser.read_project())
pprint.pprint(checker.check())

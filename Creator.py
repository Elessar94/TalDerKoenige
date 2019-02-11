import Parser
import tdk_create_onto.Knora
import Checker
import pprint


class Creator:
    project_iri = ""
    onto_iri = ""
    onto_lastmoddate = ""
    resources_iri = {}
    properties_iri = {}

    def __init__(self, file, server, user, password):
        parser = Parser.Parser(file)
        self.data = parser.read_project()
        checker = Checker.Checker(self.data)
        self.data = checker.check()
        self.interface = tdk_create_onto.Knora(server, user, password)

    def create_project(self):

        self.project_iri = self.interface.create_project(self.data['Short code'], self.data['Short name'],
                                                         self.data['Long name'], self.data['Description'],
                                                         self.data['Keywords'],
                                                         self.data['Logo'])  # is Logo in the correct format?

    def create_ontology(self):
        returns = self.interface.create_ontology(self.data['Ontology']['Name'],
                                                 self.project_iri,
                                                 self.data['Ontology']['Label'])
        self.onto_iri = returns["onto_iri"]
        self.onto_lastmoddate = returns["last_onto_date"]

    def create_resources(self):
        for resource in self.data['Ontology']['Resources']:
            returns = self.interface.create_res_class(
                self.onto_iri, self.data['Ontology']['Name'], self.onto_lastmoddate,
                resource['Name'], resource['Super classes'], resource['Labels'],
                resource['Comments'])
            self.resources_iri[resource['Name']] = returns["class_iri"]
            self.onto_lastmoddate = returns["last_onto_date"]

    def create_properties(self):
        for resource in self.data['Ontology']['Resources']:
            self.properties_iri[resource['Name']] = {}
            for property in resource['Properties']:
                returns = self.interface.create_property(self.onto_iri, self.data['Ontology']['Name'],
                                                                         self.onto_lastmoddate, property['Name'],
                                                                         property['Super Properties'],
                                                                         property['Labels'], property['GUI Element'],
                                                                         property['GUI Attributes'], resource['Name'],
                                                                         property['Object'], property['Comments'])
                self.properties_iri[resource['Name']][property['Name']] = returns["prop_iri"]
                self.onto_lastmoddate = returns["last_onto_date"]


    def link_properties_to_res(self):
        onto_name = self.data['Ontology']['Name']
        for resource in self.data['Ontology']['Resources']:
            class_iri = self.resources_iri[resource['Name']]
            for property in resource['Properties']:
                prop_iri = self.properties_iri[resource['Name']][property['Name']]
                occ = property['Cardinality']
                returns = self.interface.create_cardinality(self.onto_iri, onto_name,
                                                                          self.onto_lastmoddate, class_iri, prop_iri,
                                                                          occ)
                self.onto_lastmoddate = returns["last_onto_date"]

    def create(self):
        self.create_project()
        self.create_ontology()
        self.create_resources()
        self.create_properties()
        self.link_properties_to_res()


creator = Creator("ubkvp-onto", 0, 0, 0)
creator.create()

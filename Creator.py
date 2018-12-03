import Parser
import tdk_create_onto.Knora


class Creator:
    project_iri = ""
    onto_iri = ""
    onto_lastmoddate = ""
    resources_iri = {}
    properties_iri = {}

    def __init__(self, file, server, user, password):
        parser = Parser.Parser(file)
        self.data = parser.read_project()
        self.interface = tdk_create_onto.Knora(server, user, password)

    def create_project(self):
        self.project_iri = self.interface.create_project(self.data['Short code'], self.data['Short name'],
                                                         self.data['Long name'], self.data['Description'],
                                                         self.data['Keywords'],
                                                         self.data['Logo'])  # is Logo in the correct format?

    def create_ontology(self):
        [self.onto_iri, self.onto_lastmoddate] = self.interface.create_ontology(self.data['Ontology']['Name'],
                                                                                self.project_iri,
                                                                                self.data['Ontology']['Label'])

    def create_resources(self):
        for resource in self.data['Ontology']['Resources']:
            [self.resources_iri[resource['name']], self.onto_lastmoddate] = self.interface.create_res_class(
                self.onto_iri, self.data['Ontology']['Name'], self.onto_lastmoddate,
                resource['Name'], resource['Super classes'], resource['Labels'],
                resource['Comments'])

    def create_properties(self):
        for resource in self.data['Ontology']['Resources']:
            self.properties_iri[resource['Name']] = {}
            for property in resource['Properties']:
                [self.properties_iri[resource['Name']][property['Name']],
                 self.onto_lastmoddate] = self.interface.create_property(self.onto_iri, self.data['Ontology']['Name'],
                                                                         self.onto_lastmoddate, property['Name'],
                                                                         property['Super Properties'],
                                                                         property['Labels'], property['GUI Element'],
                                                                         property['GUI Attributes'], resource['Name'],
                                                                         property['Object'], property['Comments'])
    def link_properties_to_res(self):
        for resource in self.properties_iri:
            for property in resource:
                self.onto_lastmoddate = self.interface.create_cardinality()
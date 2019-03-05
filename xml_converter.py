class xml_converter:
    def __init__(self, planum):
        self.output = open("output_file.txt", "w")
        self.planum = planum
        #Add code for "header" of the xml-file

    def convert_planum(self):
        wb = load_workbook(self.planum)
        number = wb['A']
        position = wb['B']
        abhub = wb['C']
        planum = wb['D']
        datum = wb['E']
        campaign = wb['F']
        description = wb['G']
        remark = wb['H']
        plan = wb['I']
        image = wb['J']







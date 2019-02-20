import openpyxl
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
        for i in range(1,size(number)):
            output.write('\t<ubkvp:Planum id="') #Correct text to access planum? compare to p0801-beol of example
            output.write(number[i])
            output.write('">\n\t\t<knoraXMLImport>')
            output.write(number[i])
            output.write('</knoraXMLImport:label>\n\t\t<ubkvp:planumNr knoraType="richtext_value">')
            output.write(number[i])
            output.write("</ubkvp:planumNr\n\t\t")
            output.write('<ubkvp:planumPosition knoraType="link_value">')
            output.write(position[i])







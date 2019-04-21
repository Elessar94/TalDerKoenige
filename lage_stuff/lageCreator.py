import csv
from pprint import pprint


class lageCreator:
    def __init__(self, file):
        self.file = file

    def create_data(self):
        output = []
        with open(self.file) as csvfile:
            for line in csv.reader(csvfile, delimiter=';', quotechar='"'):
                obj = {"Grab": line[0], "Umgebung": line[1], "Areal": line[2], "Raum": line[3], "Schnitt": line[4]}
                toAdd = True
                for obj2 in output:
                    if obj["Grab"] == obj2["Grab"] and obj["Umgebung"] == obj2["Umgebung"] and obj["Areal"] == obj2[
                        "Areal"] and obj["Raum"] == obj2["Raum"] and obj["Schnitt"] == obj2["Schnitt"]:
                        toAdd = False
                        break
                if toAdd:
                    output.append(obj)
        f = open("lage_output.csv", "w+")
        for obj in output:
            str = obj["Grab"] + ";" + obj["Umgebung"] + ";" + obj["Areal"] + ";" + obj["Raum"] + ";" + obj[
                "Schnitt"] + "\n"
            f.write(str)




l = lageCreator("lageSheet.csv")
l.create_data()

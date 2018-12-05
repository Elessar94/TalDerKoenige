import sys
from typing import List, Set, Dict, Tuple, Optional
import pprint
class Checker:

    def __init__(self, dict):
        self.dict = dict
        self.can_continue = True

    def check_project(self):
        necessary_keys = {}
        possible_keys = {}
        necessary_keys['Description']= " "

        should_true = isinstance({"Hallo": "Hallo"},necessary_keys['Description'].__class__)
        print(should_true)
        pprint.pprint(necessary_keys)
        return

    def check_onto(self):
        return

    def check_res(self):
        return

    def check_prop(self):
        return

    def check_card(self):
        return

    def check(self):
        self.check_project()
        self.check_onto()
        self.check_res()
        self.check_prop()
        self.check_card()
        if not self.can_continue:
            print("Errors are fatal, can not create project. Please revise and try again.")
            sys.exit()
        return self.dict

checker = Checker(None)
checker.check()
from collections import defaultdict
import json
import os
import sys

class Data:
    REFIDS = {}
    COURSES = defaultdict(list)
    CATEGORIES = [] 

    @classmethod
    def load_data(cls, file):
        if not os.path.isfile(file) or not os.path.splitext(file)[1] == ".courses":
            return False
        if not os.path.exists("data/datafile.meta"):
            if getattr(sys, "frozen", False):
                print("Yes")
                with open(os.path.join(sys._MEIPASS, "data/datafile.meta"), "w", encoding="utf-8") as f:
                    f.write(file)
                    print(file)
        else:
            with open("data/datafile.meta", "w") as f:
                print("Here")
                f.write(file)
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
        cls.CATEGORIES = data["categories"]
        for course in data["courses"]:
            cls.REFIDS[course["name"]] = [course["refid"], 0]
            cls.COURSES[course["category"]].append(course["name"])
        return True

def last_file():
    if not os.path.exists("data/datafile.meta"):
            if getattr(sys, "frozen", False):
                with open(os.path.join(sys._MEIPASS, "data/datafile.meta"), "r", encoding="utf-8") as f:
                    return f.read()
    else:
        with open("data/datafile.meta", "r") as f:
            return f.read()


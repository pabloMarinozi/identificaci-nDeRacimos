import os

path = os.path.dirname(__file__)

with open("input.txt", 'w') as file_object:
    file_object.write(path + "/0.3.csv\n")
    file_object.write(path + "/0.4.csv\n")
    file_object.write(path + "/0.5.csv")

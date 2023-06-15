# import pygsheets
# number_plate='21BH3421AA'
# gc = pygsheets.authorize(service_file='model/number_plate.json')
# sh = gc.open('ocr')
# wks = sh.worksheet('title', 'Sheet1')  
# search_column = 'License'
# search_value = number_plate
# cell = sh.find(search_value, matchEntireCell=True)
# cell=str(cell[0][0])
# cell=cell[7:9]
# print(wks.cell((int(cell),2)).value)
# # if cell:
# #     wks.update_value('B'+cell, time_value)

import json

my_list = [[], []]

try:
    parsed_list = json.loads(my_list)
    if isinstance(parsed_list, list) and all(not sublist for sublist in parsed_list):
        print("The input is an empty list.")
    else:
        print("The input is not an empty list.")
except (json.JSONDecodeError, TypeError):
    print("The input is not a valid list.")
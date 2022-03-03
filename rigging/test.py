import json

dict = {"key1": [1, 1, 1], "key2": [2, 2, 2]}

output_path = "C:\Users\joar.engberg\Desktop\je_test.json"

with open(output_path, 'w') as outfile:
    json.dump(dict, outfile, indent=4)

load_data = json.load(open(output_path))

for key, value in load_data.iteritems():
    print(key)
    print(value)
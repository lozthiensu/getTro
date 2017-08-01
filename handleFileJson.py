import json

# Return json data
def readJson(path):
    try:
        with open(path) as fh:
            return json.load(fh)
    except Exception as e:
        print("Error", e)

# Return json data
def writeJson(path, jsonData, mode = 'w'):
    try:
        with open(path, mode) as outfile:
            json.dump(jsonData, outfile)
    except Exception as e:
        print("Error", e)
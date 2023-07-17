import json

def saveBoxes(boxes):
    f = open("save.boxes", "w")
    f.write(json.dumps(boxes))
    f.close()

def readBoxes():
    f = open("save.boxes", "r")
    boxes = json.loads(f.read())
    f.close()
    return boxes
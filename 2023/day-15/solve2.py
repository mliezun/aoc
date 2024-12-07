sequence = """rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"""

sequence = open("input.txt", "r").read().strip()


def hash(value: str) -> int:
    result = 0
    for c in value:
        result += ord(c)
        result *= 17
        result %= 256
    return result


def put_lenses_in_box(lenses):
    boxes = [{} for _ in range(256)]
    for lense in lenses:
        if lense.endswith("-"):
            label = lense[:-1]
            box = boxes[hash(label)]
            if label in box:
                del box[label]
        else:
            label, value = lense.split("=")
            boxes[hash(label)][label] = int(value)
    return boxes


def focusing_power(boxes):
    accum = 0
    for bn, box in enumerate(boxes):
        for slot, focal_length in enumerate(box.values()):
            accum += (bn + 1) * (slot + 1) * focal_length
    return accum


boxes = put_lenses_in_box([l for l in sequence.split(",")])
print("result:", focusing_power(boxes))

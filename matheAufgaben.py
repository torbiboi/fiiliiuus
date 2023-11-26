import random as r
# hässlicer code, kommentier ich später

def createTask(gType, gDifficulty):
    type = gType.split(",")
    for i in type:
        if not i in ["random", "addition", "subtraction", "multiplication", "division", "+", "-", "*", "x", ":", "/"]:
            return "ERROR2: given task type is invalid", 0
    type = r.choice(type)

    if type == "random":
        type = r.choice(["addition", "subtraction",
                        "multiplication", "division"])

    difficulty = gDifficulty.split("-")
    if len(difficulty) == 1:
        difficulty = difficulty[0]
        if int(difficulty) > 6:
            return "ERROR3: given difficulty index is out of range", 0
    elif len(difficulty) == 2:
        for i in difficulty:
            if int(i) > 6:
                return "ERROR3: given difficulty index is out of range", 0
        difficulty.sort()
        difficulty = str(r.randint(int(difficulty[0]), int(difficulty[1])))
    else:
        return "ERROR1: invalid syntax", 0

    if difficulty == "0":
        difficulty = str(r.randint(1, 6))

    if type in ["addition", "+"]:
        if difficulty == "1" or difficulty == "2" or difficulty == "3":
            paras = [r.randint(0, 10*pow(10, int(difficulty))),
                     r.randint(0, 10*pow(10, int(difficulty)))]
            question = str(paras[0]) + " + " + str(paras[1]) + " ="
        elif difficulty == "4":
            paras = [r.randint(0, 1000), r.randint(
                0, 1000), r.randint(0, 1000)]
            question = str(paras[0]) + " + " + \
                str(paras[1]) + " + " + str(paras[2]) + " ="
        elif difficulty == "5":
            paras = [r.randint(0, 10000) / pow(10, r.randint(1, 3)), r.randint(0, 10000) / pow(
                10, r.randint(1, 3)), r.randint(0, 10000) / pow(10, r.randint(1, 3))]
            question = str(paras[0]) + " + " + \
                str(paras[1]) + " + " + str(paras[2]) + " ="
        elif difficulty == "6":
            paras = [r.randint(0, 10000) / pow(10, r.randint(1, 3)), r.randint(0, 10000) / pow(
                10, r.randint(1, 3)), r.randint(0, 10000) / pow(10, r.randint(1, 3)) * -1]
            question = str(paras[0]) + " + " + \
                str(paras[1]) + " + (" + str(paras[2]) + ") ="
        return question, sum(paras)

    if type in ["subtraction", "-"]:
        if difficulty == "1" or difficulty == "2" or difficulty == "3":
            paras = [r.randint(0, pow(10, int(difficulty))),
                     r.randint(0, pow(10, int(difficulty)))]
            paras.sort()
            question = str(paras[1]) + " - " + str(paras[0]) + " ="
            result = paras[1] - paras[0]
        elif difficulty == "4":
            paras = [r.randint(0, 1000), r.randint(
                0, 1000), r.randint(0, 1000)]
            question = str(paras[0]) + " - " + \
                str(paras[1]) + " - " + str(paras[2]) + " ="
            result = paras[0] - paras[1] - paras[2]
        elif difficulty == "5":
            paras = [r.randint(0, 1000) / pow(10, r.randint(1, 2)), r.randint(0, 1000) / pow(
                10, r.randint(1, 2)), r.randint(0, 1000) / pow(10, r.randint(1, 2))]
            question = str(paras[0]) + " - " + \
                str(paras[1]) + " - " + str(paras[2]) + " ="
            result = result = paras[0] - paras[1] - paras[2]
        elif difficulty == "6":
            paras = [r.randint(0, 10000) / pow(10, r.randint(1, 3)), r.randint(0, 10000) / pow(
                10, r.randint(1, 3)), r.randint(0, 10000) / pow(10, r.randint(1, 3)) * -1]
            question = str(paras[0]) + " - " + \
                str(paras[1]) + " - (" + str(paras[2]) + ") ="
            result = result = paras[0] - paras[1] - paras[2]
        return question, result

    if type in ["multiplication", "x", "*"]:
        if difficulty == "1":
            paras = [r.randint(0, 10), r.randint(0, 10)]
            if paras[0] == paras[1]:
                question = str(paras[0]) + "² ="
            else:
                question = str(paras[0]) + " * " + str(paras[1]) + " ="
            result = paras[0] * paras[1]
        elif difficulty == "2":
            paras = [r.randint(0, 10)*pow(10, r.randint(0, 4)),
                     r.randint(0, 10)]
            if paras[0] == paras[1]:
                question = str(paras[0]) + "² ="
            else:
                question = str(paras[0]) + " * " + str(paras[1]) + " ="
            result = paras[0] * paras[1]
        elif difficulty == "3":
            paras = [r.randint(0, 10), r.randint(0, 10), r.randint(0, 10)]
            question = str(paras[0]) + " * " + \
                str(paras[1]) + " * " + str(paras[2]) + " ="
            result = paras[0] * paras[1] * paras[2]
        elif difficulty == "4":
            paras = [r.randint(0, 20), r.randint(0, 20)]
            if paras[0] == paras[1]:
                question = str(paras[0]) + "² ="
            else:
                question = str(paras[0]) + " * " + str(paras[1]) + " ="
            result = paras[0] * paras[1]
        elif difficulty == "5":
            paras = [r.randint(0, 100)/pow(10, r.randint(1, 2)),
                     r.randint(0, 20)]
            if paras[0] == paras[1]:
                question = str(paras[0]) + "² ="
            else:
                question = str(paras[0]) + " * " + str(paras[1]) + " ="
            result = paras[0] * paras[1]
        elif difficulty == "6":
            paras = [r.randint(0, 100), r.randint(0, 100)]
            if paras[0] == paras[1]:
                question = str(paras[0]) + "² ="
            else:
                question = str(paras[0]) + " * " + str(paras[1]) + " ="
            result = paras[0] * paras[1]
        return question, result

    if type in ["division", "/", ":"]:
        if difficulty == "1":
            result = r.randint(0, 10)
            paras = [r.randint(1, 10)]
            question = str(result*paras[0]) + " : " + str(paras[0]) + " ="
        elif difficulty == "2":
            paras = [r.randint(0, 100), r.randint(1, 10)]
            question = "Der Rest von: " + \
                str(paras[0]) + " : " + str(paras[1]) + "?"
            result = paras[0] % paras[1]
        elif difficulty == "3":
            result = r.randint(0, 20)
            paras = [r.randint(1, 10)]
            question = str(result*paras[0]) + " : " + str(paras[0]) + " ="
        elif difficulty == "4":
            result = r.randint(0, 20)
            paras = [r.randint(1, 20)]
            question = str(result*paras[0]) + " : " + str(paras[0]) + " ="
        elif difficulty == "5":
            result = r.randint(0, 10)
            paras = [r.randint(1, 10), r.randint(1, 10)]
            question = str(result*paras[0]*paras[1]) + " : " + \
                str(paras[0]) + " : " + str(paras[1]) + " ="
        elif difficulty == "6":
            result = r.randint(0, 100)
            paras = [r.randint(1, 100)]
            question = str(result*paras[0]) + " : " + str(paras[0]) + " ="
        return question, result
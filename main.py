import matplotlib.pyplot as plt
from matplotlib.pyplot import *


class Point:
    def __init__(self, coors, label):
        self.x = coors[0]
        self.y = coors[1]
        self.label = label

    def Draw(self):
        plot(self.x, self.y, 'ro-', linewidth=2)
        annotate(self.label, xy=(self.x + 0.3, self.y))


class LineSeg:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

    def Draw(self):
        Xcoors = [self.point1.x, self.point2.x]
        Ycoors = [self.point1.y, self.point2.y]
        plot(Xcoors, Ycoors, 'bo-', linewidth=1)
        self.point1.Draw()
        self.point2.Draw()


class Polygon:
    def __init__(self, points):
        self.points = points

    def Draw(self):
        for i, point in enumerate(self.points):
            if i + 1 == len(self.points):
                LineSeg(self.points[i], self.points[0]).Draw()
                break
            LineSeg(self.points[i], self.points[i + 1]).Draw()


class Circle:
    def __init__(self, origin, bk):
        self.origin = origin
        self.bk = bk

    def Draw(self):
        cir = plt.Circle((self.origin.x, self.origin.y), self.bk, color='b', fill=False)
        fig = plt.gcf()
        ax = fig.gca()
        ax.add_artist(cir)


def ProcessProblem1(prob):
    Ret = []
    knownSet = []
    for i in prob:
        if i == '\n':
            Ret += [knownSet]
            knownSet = []
            continue
        statement = [i.strip()]
        knownSet += statement
    Ret += [knownSet]
    return Ret


def GetPoints(known):
    Ret = []
    for i in known:
        Obj = i[1]
        Obj = [list(i) for i in Obj]
        Ret += Obj[0]
    Ret = list(set(Ret))
    return Ret


def GetLineSeg(known):
    tmp0 = []
    for i in known:
        Obj = i[1]
        tmp0 += Obj
    tmp0 = list(set(tmp0))

    Ret = []
    for i in tmp0:
        if len(i) == 1:
            continue

        for k, v in enumerate(i):
            if k + 1 == len(i):
                Ret += [[i[k], i[0]]]
                break
            Ret += [[i[k], i[k + 1]]]

    tmp0 = Ret[1:]
    Ret = [Ret[0]]
    for i in tmp0:
        exist = False
        is_same = lambda i, j: ((i[0] == j[0]) and (i[1] == j[1])) or ((i[0] == j[1]) and (i[1] == j[0]))
        tmp1 = Ret
        for j in tmp1:
            if is_same(i, j):
                exist = True
                break
        if not exist:
            Ret += [i]
    return Ret


def LoadKnowledgeBase(knowledgeFile):
    knownledgeFile = open(knowledgeFile)
    knownledge = [line.rstrip('\n') for line in knownledgeFile]
    knownledgeFile.close()

    knownledge = [i for i in knownledge if i != '']
    categorized = [[], [], []]
    for i in knownledge:
        if i == '#Objects':
            k = 0
            continue
        if i == '#Rules':
            k = 1
            continue
        if i == '#Interpreting':
            k = 2
            continue
        categorized[k] += [i]
    return categorized[0], ProcessRules(categorized[1]), ProcessInterpreting(categorized[2])


def ProcessInterpreting(interpreting):
    Ret = {}
    for i in interpreting:
        split = i.find('(')
        name = i[:split]
        param = i[split + 1:-1]
        param = param.split(',')
        param = [int(i.strip()) for i in param]
        Ret.update({name: param})
    return Ret


def ProcessRules(rules):
    Ret = []
    for i in rules:
        start = i.find('(')
        stop = i.find('):') + 2
        name = i[:start]
        val = i[stop:]
        param = i[start + 1:stop - 2]
        param = param.split(',')
        param = [i.split(':') for i in param]
        param = [[i[0].strip(), i[1].strip()] for i in param]
        rule = [name.strip(), param, val.strip()]
        Ret += [rule]

    return Ret


def PreProcessProblemSets(problemSets, Interpreting):
    Ret = []
    for problemSet in problemSets:
        tmp0 = []
        for problem in problemSet:
            tmp1 = ApplyInterpreting(Interpreting, problem)
            tmp0 += [tmp1]
        Ret += [tmp0]
    return Ret


def ApplyInterpreting(interpreting, known):
    Ret = known
    for obj in interpreting:
        pos = 0
        while True:
            start = Ret.find(obj, pos)
            if start == -1:
                break
            start += len(obj) + 1
            stop = Ret.find(')', start)
            param = list(Ret[start:stop])
            Ret = Ret[:start] + ','.join(param) + Ret[stop:]
            pos = start + 1
    return Ret


def GetRulesParam(known, rule):
    param = known
    start = pos = param.find(rule)
    counter = 0
    while True:
        open = param.find('(', pos)
        close = param.find(')', pos)
        if open < close and open != -1:
            pos = open + 1
            counter += 1
        else:
            pos = close + 1
            counter -= 1
        if counter == 0:
            stop = close
            break
    start += len(rule)
    start += 1
    param = known[start:stop]
    return param


def SplitParams1(params):
    Ret = params
    counter = pos = 0
    outside = True
    seperator = []
    while True:
        if pos == len(params):
            break
        open = params.find('(', pos)
        close = params.find(')', pos)
        seperatorx = params.find(',', pos)
        if open == close == seperatorx == -1:
            break
        if not ((seperatorx < open and seperatorx < close and seperatorx != -1) or (
                            open == close == -1 and seperatorx != -1)):
            if open < close and open != -1:
                pos = open + 1
                counter += 1
            else:
                pos = close + 1
                counter -= 1
        if counter == 0:
            pos = params.find(',', pos)
            if pos == -1:
                break
            pos += 1
            seperator += [pos]
    for i in seperator:
        Ret = Ret[:i - 1] + '|' + Ret[i + 1:]
    Ret = Ret.split('|')
    Ret = [i.strip() for i in Ret]
    return Ret


def SplitParams(params):
    Ret = params
    counter = pos = 0
    outside = True
    seperator = []
    i = 0
    counter = 0
    while True:
        if i == len(params):
            break
        if params[i] == '(':
            counter += 1
        if params[i] == ')':
            counter -= 1
        if params[i] == ',' and counter == 0:
            seperator += [i]
        i += 1
    Ret = list(Ret)
    for i in seperator:
        Ret[i] = '|'
    Ret = ''.join(Ret)
    Ret = Ret.split('|')
    Ret = [i.strip() for i in Ret]
    return Ret


def GetRuleUsingPos(known, rule):
    param = known
    start = pos = param.find(rule)
    counter = 0
    while True:
        open = param.find('(', pos)
        close = param.find(')', pos)
        if open < close and open != -1:
            pos = open + 1
            counter += 1
        else:
            pos = close + 1
            counter -= 1
        if counter == 0:
            stop = close
            break
    return start, stop


def ApplyRulesToProblem(rules, known):
    Ret = known
    while True:
        ruleFound = False
        for i in rules:
            ruleName = i[0]
            foundRule = Ret.find(ruleName)
            if foundRule == -1:
                continue
            ruleFound = True
            start, stop = GetRuleUsingPos(Ret, ruleName)
            params = GetRulesParam(Ret, ruleName)
            params = SplitParams(params)

            replacement = i[2]
            k = 0
            while True:
                if k == len(replacement):
                    break
                for j, v in enumerate(i[1]):
                    if v[0] == replacement[k] and (
                                            replacement[k + 1] == ' ' or replacement[k + 1] == ',' or replacement[
                                        k + 1] == ')' or replacement[k + 1] == '.'):
                        replacement = replacement[:k] + params[j] + replacement[k + 1:]
                        k += len(params[j])
                k += 1

            Ret = Ret[:start] + replacement + Ret[stop + 1:]
        if ruleFound == False:
            break

    print(Ret)

    return Ret


def ApplyRulesToProblemSet(rules, problemSet):
    Ret = [[ApplyRulesToProblem(rules, j) for j in i] for i in problemSet]
    return Ret


def GetObjects(object, known):
    Ret = []
    return Ret


def variablename(var):
    return [tpl[0] for tpl in filter(lambda x: var is x[1], globals().items())][0]


def printx(var):
    print(variablename(var) + ':')
    print(var)


Objects, Rules, Interpreting = LoadKnowledgeBase('Knowledge.kb')
# print(Objects)
# print(Rules)

# print("Nhập đề bài\n")
# known = []
# while True:
#     line = input()
#     if line:
#         known += [line]
#     else:
#         break
known = open('probs1.txt').readlines()
problemSets = ProcessProblem1(known)
problemSets = PreProcessProblemSets(problemSets, Interpreting=Interpreting)
problemSets = ApplyRulesToProblemSet(Rules, problemSets)

printx(problemSets)
# known = ApplyInterpreting(Interpreting, known)
# print(known)
# points = GetPoints(known)
# lineSeg = GetLineSeg(known)

# A = Point([14, 1], 'A')
# B = Point([4, 12], 'B')
# C = Point([9, 3], 'C')
# A.Draw()
# B.Draw()
# C.Draw()
# poly = Polygon([A, B, C])
# poly.Draw()
# cir = Circle(A, 4)
# cir.Draw()
# axis([0, 10, 0, 10])
# legend()
# plt.axis('scaled')
# matplotlib.pyplot.show()

import matplotlib.pyplot as plt
from matplotlib.pyplot import *
from sympy import *
import random

rangeOfRand = 5
randomizedValue = []


class PointX:
    def __init__(self, coors, label=None):
        self.x = coors[0]
        self.y = coors[1]
        self.label = label

    def Draw(self):
        plt.plot(self.x, self.y, 'ro-', linewidth=2)
        if self.label != None:
            plt.annotate(self.label, xy=(self.x + 0.3, self.y))


class LineSegX:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

    def Draw(self):
        Xcoors = [self.point1.x, self.point2.x]
        Ycoors = [self.point1.y, self.point2.y]
        plt.plot(Xcoors, Ycoors, 'bo-', linewidth=1)
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


class CircleX:
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


def GetConstraint(known, Constraint):
    known0 = known
    Ret = []
    while True:
        ConstraintFound = False
        for i in Constraint:
            ruleName = i[0]
            foundRule = known0.find(ruleName)
            if foundRule == -1:
                continue
            ConstraintFound = True
            start, stop = GetRuleUsingPos(known0, ruleName)
            params = GetRulesParam(known0, ruleName)
            params = SplitParams(params)

            replacement = i[2]
            k = 0
            while True:
                if k >= len(replacement):
                    break
                for j, v in enumerate(i[1]):
                    if v[0] == replacement[k] and (
                                            replacement[k + 1] == ' ' or replacement[k + 1] == ',' or replacement[
                                        k + 1] == ')' or replacement[k + 1] == '.'):
                        replacement = replacement[:k] + params[j] + replacement[k + 1:]
                        k += len(params[j])
                k += 1
            Ret += [replacement]
            known0 = known0[:start] + known0[stop + 1:]
        if ConstraintFound == False:
            break

    return Ret


def LoadKnowledgeBase(knowledgeFile):
    knownledgeFile = open(knowledgeFile)
    knownledge = [line.rstrip('\n') for line in knownledgeFile]
    knownledgeFile.close()

    knownledge = [i for i in knownledge if i != '']
    categorized = [[], [], [], [], [], [], []]
    for i in knownledge:
        if i == '#Objects':
            k = 0
            continue
        if i == '#Rules':
            k = 1
            continue
        if i == '#Rules0':
            k = 2
            continue
        if i == '#Interpreting':
            k = 3
            continue
        if i == '#Constraint':
            k = 4
            continue
        if i == '#Constructings':
            k = 5
            continue
        if i == '#Drawings':
            k = 6
            continue
        categorized[k] += [i]
    return ProcessObjects(categorized[0]), ProcessRules(categorized[1]), ProcessRules(
        categorized[2]), ProcessInterpreting(
        categorized[3]), ProcessRules(categorized[4]), ProcessRules(categorized[5]), ProcessDrawing(categorized[6])


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


def ProcessDrawing(rules):
    Ret = []
    for i in rules:
        start = i.find('(')
        stop = i.find(')') + 1
        name = i[:start]
        param = i[start + 1:stop - 1]
        param = param.split(',')
        param = [i.split(':')[0] for i in param]
        param = [i.strip() for i in param]
        rule = [name.strip(), param]
        Ret += [rule]

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


def ProcessObjects(objects):
    Ret = []
    for i in objects:
        colon = i.rfind(':')
        name = i[:colon].strip()
        param = name[name.find('(') + 1:-1]
        name = name[:name.find('(')]
        param = param.split(',')
        param = [i[:i.find(':')].strip() for i in param]
        att = i[colon + 1:].strip()
        att = att.split(',')
        att = [i.split('=') for i in att]
        att = [[j.strip() for j in i] for i in att]
        att = {i[0]: i[1] for i in att}
        obj = [name, param, att]
        Ret += [obj]

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
    start = stop = pos = known.find(rule)
    i = start
    counter = 0
    inside = False
    while True:
        i += 1
        if i == len(known):
            break
        if known[i] == '(':
            inside = True
            counter += 1
        if known[i] == ')':
            counter -= 1
        if counter == 0 and inside:
            stop = i
            break

    return start, stop


def GetRuleUsingPos1(known, rule):
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


def ApplyRulesToProblem(rules, constraint, known, Constraint):
    Ret = known
    while True:
        ruleFound = False
        for i in rules:
            RetConstraint = GetConstraint(Ret, constraint)
            Constraint.update(set(RetConstraint))
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
                if k >= len(replacement):
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

    return Ret


def ApplyRules0ToProblem(rules, known):
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
            Ret = Ret[:start + len(ruleName) + 1] + Ret[start + len(ruleName) + 2:stop - 1] + Ret[stop:]
            start, stop = GetRuleUsingPos(Ret, ruleName)
            params = GetRulesParam(Ret, ruleName)
            params = SplitParams(params)

            replacement = i[2]
            k = 0
            while True:
                if k >= len(replacement):
                    break
                for j, v in enumerate(i[1]):
                    if k >= len(replacement):
                        break
                    if v[0] == replacement[k]:
                        if k + 1 != len(replacement):
                            if (replacement[k + 1] != ' ' and replacement[k + 1] != ',' and replacement[
                                    k + 1] != ')' and replacement[k + 1] != '.'):
                                continue
                        replacement = replacement[:k] + params[j] + replacement[k + 1:]
                        k += len(params[j])
                k += 1

            Ret = Ret[:start] + replacement + Ret[stop + 1:]
            pass
        if ruleFound == False:
            break

    return Ret


def SplitProblem(problem):
    Ret = problem.split(';')
    Ret = [i.strip() for i in Ret]
    return Ret


def PrintProblemSet(problemSet):
    for i in problemSet:
        for j in i:
            print(j)
        print('\n')


def EquationToExpression(equa):
    Ret = equa.replace('.', '').replace('==', '-(')
    Ret = Ret + ')'
    return Ret


def GetSymbols(expr):
    return expr.free_symbols


def ProcessConstraints(Constraint):
    Ret = []
    for i in Constraint:
        Ret += i.split(';')
    Ret = [i.strip() for i in Ret]

    return Ret


def ApplyRulesToProblemSet(rules, rules0, objects, constraint, problemSet):
    Constraint = set()
    tmp = [[ApplyRulesToProblem(rules, constraint, j, Constraint) for j in i] for i in problemSet]
    Constraint = list(Constraint)
    Constraint = ProcessConstraints(Constraint)
    # Constraint = [ApplyRulesToProblem(constraint, constraint, i, set()) for i in Constraint]
    Constraint = [ApplyRules0ToProblem(rules0, i) for i in Constraint]
    Constraint = [ApplyObjects(objects, i) for i in Constraint]
    Constraint = [i.replace('.', '') for i in Constraint]
    Constraint = [sympify(i.split('!=')[0] + '-' + i.split('!=')[1]) if i.find('!=') != -1 else sympify(i) for i in
                  Constraint]
    Constraint = [[i, str(GetSymbols(sympify(i))).replace('{', '').replace('}', '').split(',')] for i in Constraint]
    Constraint = [[i[0], [j.strip() for j in i[1]]] for i in Constraint]
    tmp = [[ApplyRules0ToProblem(rules0, j) for j in i] for i in tmp]
    tmp = [[ApplyObjects(objects, j) for j in i] for i in tmp]
    Ret = []
    for i in tmp:
        tmp1 = []
        for j in i:
            semicolon = j.find(';')
            if semicolon != -1:
                tmp2 = j.split(';')
                tmp2 = [k.strip() for k in tmp2]
            else:
                tmp2 = [j]
            tmp1 += tmp2
        Ret += [tmp1]
    Ret = [[EquationToExpression(j) for j in i if j != ''] for i in Ret]
    Ret = [
        [[j, [k.strip() for k in str(GetSymbols(sympify(j))).replace('{', '').replace('}', '').split(',')]] for j in i]
        for i in Ret]

    return Ret, Constraint


def ApplyObjects(objects, problem):
    Ret = problem

    while True:
        foundRule = False
        for i in objects:
            name = i[0]
            start, stop = GetRuleUsingPos(Ret, name)
            if start == -1:
                continue
            foundRule = True
            stop += 1
            if Ret[stop] == '.':
                stop += 1
            stopSymbol = ['*', ' ', '=', '+', '-', ')', ',', '^', '.']
            SymbolPos = [Ret.find(j, stop) for j in stopSymbol]
            SymbolPos = [j for j in SymbolPos if j != -1]
            if (len(SymbolPos) == 0):
                stop = len(Ret) - 1
            else:
                stop = min(SymbolPos) - 1
            params = SplitParams(GetRulesParam(Ret, name))
            replacement = Ret[Ret.rfind(').', 0, stop) + 2:stop + 1]
            replacement = replacement.split('.')[0]
            replacement = i[2][replacement]

            k = 0
            while True:
                if k >= len(replacement):
                    break
                for j, v in enumerate(i[1]):
                    if v == replacement[k]:
                        replacement = replacement[:k] + params[j] + replacement[k + 1:]
                        k += len(params[j])
                        break
                k += 1
            Ret = Ret[:start] + replacement + Ret[stop + 1:]
            pass
        if not foundRule:
            break

    return Ret


def SolveProblemSet(problemSet, constraint):
    Ret = problemSets
    Sol = {}
    Ret = [sorted(i, key=lambda x: len(x[1])) for i in Ret]
    for i in Ret:
        while True:
            found2 = False
            found0 = True
            while len(i) > 1 and found0:
                found0 = False
                for j in range(len(i) - 1):
                    paramsJ = set(i[j][1]) - set(Sol)
                    found = False
                    for k in range(j + 1, len(i)):
                        paramsK = set(i[k][1]) - set(Sol)
                        if paramsJ == paramsK and len(paramsJ) != 0:
                            solved = True
                            while True:
                                unknown = paramsJ - set(Sol)
                                numofunknown = len(unknown)
                                if numofunknown > 2:
                                    GenerateUnknown(Sol, next(iter(unknown)), constraint)
                                elif numofunknown == 2:
                                    solved = SolveEquationSystem([i[k][0], i[j][0]], Sol, constraint)
                                    break
                            if solved:
                                found2 = True
                                i.remove(i[k])
                                i.remove(i[j])
                                found = True
                                break
                    if found:
                        found0 = True
                        break
            found1 = False
            for j in i:
                while True:
                    unknown = set(j[1]) - set(Sol)
                    numofunknown = len(unknown)
                    if numofunknown > 1:
                        GenerateUnknown(Sol, next(iter(unknown)), constraint)
                    elif numofunknown == 1:
                        solvable = SolveEquation(j[0], Sol, constraint)
                        if not solvable:
                            continue
                        found1 = True
                        break
                    if numofunknown == 0:
                        break
            if not found2 and not found1:
                break
    return Sol


def SolveEquationSystem(sys, solution, constraint):
    Ret = [sympify(i).subs(solution) for i in sys]
    Ret = solve(Ret, dict=True)
    if len(Ret) == 0:
        tmp1 = randomizedValue.pop()
        solution.pop(tmp1[0])
        for i in tmp1[1]:
            solution.pop(i)
        return False
    Ret = Ret[0] if type(Ret) is list else Ret
    Ret0 = {}
    for i in Ret:
        if Ret[i].as_real_imag()[1] != 0:
            tmp1 = randomizedValue.pop()
            solution.pop(tmp1[0])
            for i in tmp1[1]:
                solution.pop(i)
            return False
        tmp = randomizedValue.pop()
        tmp[1].append(str(i))
        randomizedValue.append(tmp)
        item = {str(i): Ret[i]}
        Ret0.update(item)

    solution.update(Ret0)
    return True


def SolveEquation(equa, solution, constraint):
    Ret = sympify(equa).subs(solution)
    Ret0 = solve(Ret, dict=True)
    if len(Ret0) == 0:
        tmp1 = randomizedValue.pop()
        solution.pop(tmp1[0])
        for i in tmp1[1]:
            solution.pop(i)
        return False
    for i in Ret0:
        sol = Ret0[0]
        k = next(iter(sol))
        tmp = randomizedValue.pop()
        tmp[1].append(str(k))
        randomizedValue.append(tmp)
        sol = {str(k): sol[k]}
        tmp = solution
        tmp.update(sol)
        if CheckConstraint(tmp, constraint):
            solution.update(sol)
            break
    return True


def GenerateUnknown(solution, unknown, constraint):
    while True:
        tmp1 = solution
        global rangeOfRand
        tmp0 = random.randint(-rangeOfRand, rangeOfRand)
        rangeOfRand += 1
        if rangeOfRand == 1000:
            rangeOfRand = 5
        tmp1.update({unknown: tmp0})
        global randomizedValue
        randomizedValue.append([unknown, []])
        if CheckConstraint(tmp1, constraint):
            solution.update(tmp1)
            break


def CheckConstraint(solution, constraint):
    keys = set(solution.keys())
    sastisfied = True
    for i in constraint:
        constraintKeys = set(i[1])
        if len(constraintKeys - keys) == 0:
            constr = i[0]
            constr = constr.subs(solution)
            if constr.is_Boolean:
                sastisfied = constr
            else:
                sastisfied = True if constr != 0 else False
            if not sastisfied:
                break
    return sastisfied


def variablename(var):
    return [tpl[0] for tpl in filter(lambda x: var is x[1], globals().items())][0]


def printx(var):
    print(variablename(var) + ':')
    print(var)


def constructObject(problemSets, constructings, rules0):
    Ret0 = []
    for i in problemSets:
        for j in i:
            Ret = j
            while True:
                ruleFound = False
                for i in constructings:
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
                        if k >= len(replacement):
                            break
                        for j, v in enumerate(i[1]):
                            if v[0] == replacement[k] and (
                                                    replacement[k + 1] == ' ' or replacement[k + 1] == ',' or
                                                replacement[
                                                        k + 1] == ')' or replacement[k + 1] == '.'):
                                replacement = replacement[:k] + params[j] + replacement[k + 1:]
                                k += len(params[j])
                        k += 1
                    Ret0 += [replacement]
                    Ret = Ret[stop + 1:]
                if ruleFound == False:
                    break
    Ret0 = [ApplyRules0ToProblem(rules0, i) for i in Ret0]
    Ret1 = []
    for i in Ret0:
        a = i.split(';')
        if len(a) > 1:
            a = [k.strip() for k in a]
        Ret1 += a
    Ret2 = []
    for i in Ret1:
        start = i.find('(')
        name = i[:start]
        params = i[start + 1:-1].split(',')
        params = [i.strip() for i in params]
        tmp = [name, params]
        Ret2 += [tmp]
    return Ret2


def getObjects(problemSets, objects):
    Ret0 = []
    for i in problemSets:
        for j in i:
            k = 0
            while True:
                Ret = j[k:]
                foundRule = False
                for i in objects:
                    name = i[0]
                    if name == 'Vector':
                        continue
                    start, stop = GetRuleUsingPos(Ret, name)
                    if start == -1:
                        continue
                    foundRule = True
                    stop += 1
                    if Ret[stop] == '.':
                        stop += 1
                    k += stop
                    params = SplitParams(GetRulesParam(Ret, name))
                    obj = [name, params]
                    Ret0 += [obj]
                if not foundRule:
                    break
    Ret1 = []
    for i in Ret0:
        found = False
        for j in Ret1:
            if i[0] == j[0]:
                a = set(i[1])
                b = set(j[1])
                if a <= b and b <= a:
                    found = True
                    break
        if not found:
            Ret1 += [i]
    return Ret1


def Drawing(points, object):
    Points = {}
    for i in points:
        if i[-1] == 'x' or i[-1] == 'y':
            tmp = i[0]
            tmp = {i[-1]: points[i]}
            val = Points.get(i[0], -1)
            if val == -1:
                tmp2 = {i[0]: tmp}
                Points.update(tmp2)
            else:
                tmp1 = Points[i[0]]
                tmp1.update(tmp)
        else:
            Points.update({i: points[i]})

    for i in Points:
        if type(Points[i]) is dict:
            p = PointX([Points[i]['x'], Points[i]['y']], i)
            p.Draw()
    for i in object:
        if i[0] == 'DoanThang':
            s = LineSegX(PointX([Points[i[1][0]]['x'], Points[i[1][0]]['y']]),
                         PointX([Points[i[1][1]]['x'], Points[i[1][1]]['y']]))
            s.Draw()
        if i[0] == 'DuongTron':
            s = CircleX(PointX([Points[i[1][0]]['x'], Points[i[1][0]]['y']]), Points[i[1][1]])
            s.Draw()

    # A = Point([14, 1], 'A')
    # A.Draw()
    # poly = Polygon([A, B, C])
    # poly.Draw()
    # cir = Circle(A, 4)
    # cir.Draw()
    # axis([0, 10, 0, 10])
    # legend()
    axis([-20, 20, -20, 20])
    plt.axis('scaled')
    plt.show()
    print('')
    pass


Objects, Rules, Rules0, Interpreting, Constraint, Constructing, Drawings = LoadKnowledgeBase('Knowledge.kb')

known = open('probs1.txt').readlines()
problemSets = ProcessProblem1(known)
problemSets = PreProcessProblemSets(problemSets, Interpreting=Interpreting)
construct = constructObject(problemSets, Constructing, Rules0)
problemSets, constraint = ApplyRulesToProblemSet(Rules, Rules0, Objects, Constraint, problemSets)
Points = SolveProblemSet(problemSets, constraint)
Drawing(Points, construct)
# TODO: solve abs() equation

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

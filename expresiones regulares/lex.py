from os import popen
import time

class Automata:

    def __init__(self, language = set(['0', '1'])):
        self.states = set()
        self.startstate = None
        self.finalstates = []
        self.transitions = dict()
        self.language = language

    @staticmethod
    def epsilon():
        return "e"

    def setstartstate(self, state):
        self.startstate = state
        self.states.add(state)

    def addfinalstates(self, state):
        if isinstance(state, int):
            state = [state]
        for s in state:
            if s not in self.finalstates:
                self.finalstates.append(s)

    def addtransition(self, fromstate, tostate, inp):
        if isinstance(inp, str):
            inp = set([inp])
        self.states.add(fromstate)
        self.states.add(tostate)
        if fromstate in self.transitions:
            if tostate in self.transitions[fromstate]:
                self.transitions[fromstate][tostate] = self.transitions[fromstate][tostate].union(inp)
            else:
                self.transitions[fromstate][tostate] = inp
        else:
            self.transitions[fromstate] = {tostate : inp}

    def addtransition_dict(self, transitions):
        for fromstate, tostates in transitions.items():
            for state in tostates:
                self.addtransition(fromstate, state, tostates[state])

    def gettransitions(self, state, key):
        if isinstance(state, int):
            state = [state]
        trstates = set()
        for st in state:
            if st in self.transitions:
                for tns in self.transitions[st]:
                    if key in self.transitions[st][tns]:
                        trstates.add(tns)
        return trstates

    def getEClose(self, findstate):
        allstates = set()
        states = set([findstate])
        while len(states)!= 0:
            state = states.pop()
            allstates.add(state)
            if state in self.transitions:
                for tns in self.transitions[state]:
                    if Automata.epsilon() in self.transitions[state][tns] and tns not in allstates:
                        states.add(tns)
        return allstates

    def display(self):
        print "estados:", self.states
        print "estado inicial: ", self.startstate
        print "estado final:", self.finalstates
        print "transiciones:"
        for fromstate, tostates in self.transitions.items():
            for state in tostates:
                for char in tostates[state]:
                    print "  ",fromstate, "->", state, "on '"+char+"'",
            print

    def getPrintText(self):
        text = "leguaje: {" + ", ".join(self.language) + "}\n"
        text += "estados: {" + ", ".join(map(str,self.states)) + "}\n"
        text += "estado inicial: " + str(self.startstate) + "\n"
        text += "estado final: {" + ", ".join(map(str,self.finalstates)) + "}\n"
        text += "transiciones:\n"
        linecount = 5
        for fromstate, tostates in self.transitions.items():
            for state in tostates:
                for char in tostates[state]:
                    text += "    " + str(fromstate) + " -> " + str(state) + " on '" + char + "'\n"
                    linecount +=1
        return [text, linecount]

    def newBuildFromNumber(self, startnum):
        translations = {}
        for i in list(self.states):
            translations[i] = startnum
            startnum += 1
        rebuild = Automata(self.language)
        rebuild.setstartstate(translations[self.startstate])
        rebuild.addfinalstates(translations[self.finalstates[0]])
        for fromstate, tostates in self.transitions.items():
            for state in tostates:
                rebuild.addtransition(translations[fromstate], translations[state], tostates[state])
        return [rebuild, startnum]

    def newBuildFromEquivalentStates(self, equivalent, pos):
        rebuild = Automata(self.language)
        for fromstate, tostates in self.transitions.items():
            for state in tostates:
                rebuild.addtransition(pos[fromstate], pos[state], tostates[state])
        rebuild.setstartstate(pos[self.startstate])
        for s in self.finalstates:
            rebuild.addfinalstates(pos[s])
        return rebuild

    def getDotFile(self):
        dotFile = "digraph afd {\nrankdir=LR\n"
        if len(self.states) != 0:
            dotFile += "root=s1\nstart [shape=point]\nstart->s%d\n" % self.startstate
            for state in self.states:
                if state in self.finalstates:
                    dotFile += "s%d [shape=doublecircle]\n" % state
                else:
                    dotFile += "s%d [shape=circle]\n" % state
            for fromstate, tostates in self.transitions.items():
                for state in tostates:
                    for char in tostates[state]:
                        dotFile += 's%d->s%d [label="%s"]\n' % (fromstate, state, char)
        dotFile += "}"
        return dotFile

class BuildAutomata:


    @staticmethod
    def basicstruct(inp):
        state1 = 1
        state2 = 2
        basic = Automata()
        basic.setstartstate(state1)
        basic.addfinalstates(state2)
        basic.addtransition(1, 2, inp)
        return basic

    @staticmethod
    def plusstruct(a, b):
        [a, m1] = a.newBuildFromNumber(2)
        [b, m2] = b.newBuildFromNumber(m1)
        state1 = 1
        state2 = m2
        plus = Automata()
        plus.setstartstate(state1)
        plus.addfinalstates(state2)
        plus.addtransition(plus.startstate, a.startstate, Automata.epsilon())
        plus.addtransition(plus.startstate, b.startstate, Automata.epsilon())
        plus.addtransition(a.finalstates[0], plus.finalstates[0], Automata.epsilon())
        plus.addtransition(b.finalstates[0], plus.finalstates[0], Automata.epsilon())
        plus.addtransition_dict(a.transitions)
        plus.addtransition_dict(b.transitions)
        return plus

    @staticmethod
    def dotstruct(a, b):
        [a, m1] = a.newBuildFromNumber(1)
        [b, m2] = b.newBuildFromNumber(m1)
        state1 = 1
        state2 = m2-1
        dot = Automata()
        dot.setstartstate(state1)
        dot.addfinalstates(state2)
        dot.addtransition(a.finalstates[0], b.startstate, Automata.epsilon())
        dot.addtransition_dict(a.transitions)
        dot.addtransition_dict(b.transitions)
        return dot

    @staticmethod
    def starstruct(a):
        [a, m1] = a.newBuildFromNumber(2)
        state1 = 1
        state2 = m1
        star = Automata()
        star.setstartstate(state1)
        star.addfinalstates(state2)
        star.addtransition(star.startstate, a.startstate, Automata.epsilon())
        star.addtransition(star.startstate, star.finalstates[0], Automata.epsilon())
        star.addtransition(a.finalstates[0], star.finalstates[0], Automata.epsilon())
        star.addtransition(a.finalstates[0], a.startstate, Automata.epsilon())
        star.addtransition_dict(a.transitions)
        return star


class afdfromafnd:

    def __init__(self, afnd):
        self.buildafd(afnd)
        self.minimise()

    def getafd(self):
        return self.afd

    def getMinimisedafd(self):
        return self.minafd

    def displayafd(self):
        self.afd.display()

    def displayMinimisedafd(self):
        self.minafd.display()

    def buildafd(self, afnd):
        allstates = dict()
        eclose = dict()
        count = 1
        state1 = afnd.getEClose(afnd.startstate)
        eclose[afnd.startstate] = state1
        afd = Automata(afnd.language)
        afd.setstartstate(count)
        states = [[state1, count]]
        allstates[count] = state1
        count +=  1
        while len(states) != 0:
            [state, fromindex] = states.pop()
            for char in afd.language:
                trstates = afnd.gettransitions(state, char)
                for s in list(trstates)[:]:
                    if s not in eclose:
                        eclose[s] = afnd.getEClose(s)
                    trstates = trstates.union(eclose[s])
                if len(trstates) != 0:
                    if trstates not in allstates.values():
                        states.append([trstates, count])
                        allstates[count] = trstates
                        toindex = count
                        count +=  1
                    else:
                        toindex = [k for k, v in allstates.iteritems() if v  ==  trstates][0]
                    afd.addtransition(fromindex, toindex, char)
        for value, state in allstates.iteritems():
            if afnd.finalstates[0] in state:
                afd.addfinalstates(value)
        self.afd = afd

    def acceptsString(self, string):
        currentstate = self.afd.startstate
        for ch in string:
            if ch=="e":
                continue
            st = list(self.afd.gettransitions(currentstate, ch))
            if len(st) == 0:
                return False
            currentstate = st[0]
        if currentstate in self.afd.finalstates:
            return True
        return False

    def minimise(self):
        states = list(self.afd.states)
        n = len(states)
        unchecked = dict()
        count = 1
        distinguished = []
        equivalent = dict(zip(range(len(states)), [{s} for s in states]))
        pos = dict(zip(states,range(len(states))))
        for i in range(n-1):
            for j in range(i+1, n):
                if not ([states[i], states[j]] in distinguished or [states[j], states[i]] in distinguished):
                    eq = 1
                    toappend = []
                    for char in self.afd.language:
                        s1 = self.afd.gettransitions(states[i], char)
                        s2 = self.afd.gettransitions(states[j], char)
                        if len(s1) != len(s2):
                            eq = 0
                            break
                        if len(s1) > 1:
                            raise BaseException("afd transiciones multiples")
                        elif len(s1) == 0:
                            continue
                        s1 = s1.pop()
                        s2 = s2.pop()
                        if s1 != s2:
                            if [s1, s2] in distinguished or [s2, s1] in distinguished:
                                eq = 0
                                break
                            else:
                                toappend.append([s1, s2, char])
                                eq = -1
                    if eq == 0:
                        distinguished.append([states[i], states[j]])
                    elif eq == -1:
                        s = [states[i], states[j]]
                        s.extend(toappend)
                        unchecked[count] = s
                        count += 1
                    else:
                        p1 = pos[states[i]]
                        p2 = pos[states[j]]
                        if p1 != p2:
                            st = equivalent.pop(p2)
                            for s in st:
                                pos[s] = p1
                            equivalent[p1] = equivalent[p1].union(st)
        newFound = True
        while newFound and len(unchecked) > 0:
            newFound = False
            toremove = set()
            for p, pair in unchecked.items():
                for tr in pair[2:]:
                    if [tr[0], tr[1]] in distinguished or [tr[1], tr[0]] in distinguished:
                        unchecked.pop(p)
                        distinguished.append([pair[0], pair[1]])
                        newFound = True
                        break
        for pair in unchecked.values():
            p1 = pos[pair[0]]
            p2 = pos[pair[1]]
            if p1 != p2:
                st = equivalent.pop(p2)
                for s in st:
                    pos[s] = p1
                equivalent[p1] = equivalent[p1].union(st)
        if len(equivalent) == len(states):
            self.minafd = self.afd
        else:
            self.minafd = self.afd.newBuildFromEquivalentStates(equivalent, pos)

class afndfromRegex:

    def __init__(self, regex):
        self.star = '*'
        self.plus = '+'
        self.dot = '.'
        self.opBracket = '('
        self.clBracket = ')'
        self.operators = [self.plus, self.dot]
        self.regex = regex
        self.alphabet = [chr(i) for i in range(65,91)]
        self.alphabet.extend([chr(i) for i in range(97,123)])
        self.alphabet.extend([chr(i) for i in range(48,58)])
        self.buildafnd()

    def getafnd(self):
        return self.afnd

    def displayafnd(self):
        self.afnd.display()

    def buildafnd(self):
        language = set()
        self.stack = []
        self.automata = []
        previous = "::e::"
        for char in self.regex:
            if char in self.alphabet:
                language.add(char)
                if previous != self.dot and (previous in self.alphabet or previous in [self.clBracket,self.star]):
                    self.addOperatorToStack(self.dot)
                self.automata.append(BuildAutomata.basicstruct(char))
            elif char  ==  self.opBracket:
                if previous != self.dot and (previous in self.alphabet or previous in [self.clBracket,self.star]):
                    self.addOperatorToStack(self.dot)
                self.stack.append(char)
            elif char  ==  self.clBracket:
                if previous in self.operators:
                    raise BaseException("Error '%s' despues '%s'" % (char, previous))
                while(1):
                    if len(self.stack) == 0:
                        raise BaseException("Error '%s'. stack vacio" % char)
                    o = self.stack.pop()
                    if o == self.opBracket:
                        break
                    elif o in self.operators:
                        self.processOperator(o)
            elif char == self.star:
                if previous in self.operators or previous  == self.opBracket or previous == self.star:
                    raise BaseException("Error '%s' despues '%s'" % (char, previous))
                self.processOperator(char)
            elif char in self.operators:
                if previous in self.operators or previous  == self.opBracket:
                    raise BaseException("Error '%s' despues '%s'" % (char, previous))
                else:
                    self.addOperatorToStack(char)
            else:
                raise BaseException("Simbolo '%s' no esta definido" % char)
            previous = char
        while len(self.stack) != 0:
            op = self.stack.pop()
            self.processOperator(op)
        if len(self.automata) > 1:
            print self.automata
            raise BaseException("Expresion regular tuvo un error")
        self.afnd = self.automata.pop()
        self.afnd.language = language

    def addOperatorToStack(self, char):
        while(1):
            if len(self.stack) == 0:
                break
            top = self.stack[len(self.stack)-1]
            if top == self.opBracket:
                break
            if top == char or top == self.dot:
                op = self.stack.pop()
                self.processOperator(op)
            else:
                break
        self.stack.append(char)

    def processOperator(self, operator):
        if len(self.automata) == 0:
            raise BaseException("Error  '%s'. Stack esta vacio" % operator)
        if operator == self.star:
            a = self.automata.pop()
            self.automata.append(BuildAutomata.starstruct(a))
        elif operator in self.operators:
            if len(self.automata) < 2:
                raise BaseException("Error  '%s'. operacion inadecuada" % operator)
            a = self.automata.pop()
            b = self.automata.pop()
            if operator == self.plus:
                self.automata.append(BuildAutomata.plusstruct(b,a))
            elif operator == self.dot:
                self.automata.append(BuildAutomata.dotstruct(b,a))

def drawGraph(automata, file = ""):
    f = popen(r"dot -Tpng -o graph%s.png" % file, 'w')
    try:
        f.write(automata.getDotFile())
    except:
        raise BaseException("Error creating graph")
    finally:
        f.close()

def isInstalled(program):
    import os
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)
    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program) or is_exe(program+".exe"):
            return True
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file) or is_exe(exe_file+".exe"):
                return True
    return False

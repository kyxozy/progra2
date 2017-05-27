
from lex import *
import sys

def main():
    inp = "(2*+1)*"
    if len(sys.argv)>1:
        inp = sys.argv[1]
    print "Regular Expression: ", inp
    afndObj = afndfromRegex(inp)
    afnd = afndObj.getafnd()
    afdObj = afdfromafnd(afnd)
    afd = afdObj.getafd()
    minafd = afdObj.getMinimisedafd()
    print "\nafnd: "
    afndObj.displayafnd()
    print "\nafd: "
    afdObj.displayafd()
    print "\nMinimised afd: "
    afdObj.displayMinimisedafd()
    if isInstalled("dot"):
        drawGraph(afd, "afd")
        drawGraph(afnd, "afnd")
        drawGraph(minafd, "mafd")
        print "\nGraphs ha sido creada"
        print minafd.getDotFile()

if __name__  ==  '__main__':
    t = time.time()
    try:
        main()
    except BaseException as e:
        print "\nError:", e
    print "\nTiempo: ", time.time() - t, "segundos"

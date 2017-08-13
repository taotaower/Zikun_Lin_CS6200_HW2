import math


f=open('Task1-G1.txt') # open G1
#f=open('wt2g_inlinks.txt') # open G2
#f=open('test.txt') # open G1
eGraph = []
M = {}
L = {}


while 1:
    file = f.readline()
    if file:
        list = file.split(' ')
        list = filter(lambda x: x != '\n', list)
        list = map(lambda x: x.replace('\n', ''), list)
        list = map(lambda x: x.replace('\r', ''), list)

        eGraph.extend([[i,list[0]] for i in list[1:]])
        M[list[0]] = list[1:]

    else:
        break


def pageRank (d):

    P = set([j for i in eGraph for j in i]) # set of all pages
    print 'P:', P, len(P)

    N = len(P)
    notSourceNodes = set([i[1] for i in eGraph])
#    print 'notSourceNodes:' , notSourceNodes
    notSinkNodes = set([i[0] for i in eGraph])
    sources = set(P).difference(notSourceNodes)
#    print 'SourceNodes:', sources

#    print 'notSinkNodes:', P
    S = set(P).difference(notSinkNodes) # sinkNodes
    statReport(sources,S,N)
#    print 'sink nodes:', S

    PR = {}.fromkeys(P, 1 / float(N))  # initial PG-values for each pages
    newPR = {}
    for p in notSinkNodes :
        L[p] = getL(p)

    totalPerps = []
    perps = []
    perplexity = 2 ** (H(PR))
    totalPerps.append(perplexity)
    perps.append(perplexity)



    while not converge(perps): # implement the algorithm
        sinkPR = 0
        for p in S:
            sinkPR += PR[p]
        for p in P:
            newPR[p] = (1 - d) / float(N)  # teleportation
            newPR[p] += d * sinkPR / float(N) # spread remaining sink PR evenly
            if M.has_key(p):
                for q in M[p]:  # M(p) is the set (without duplicates) of pages that link to page p
                    newPR[p] += d * PR[q] / float(L[q])
        for p in P:
            PR[p] = newPR[p]
        perplexity = 2 ** (H(PR))
        totalPerps.append(perplexity)
        perps.append(perplexity)

    writePerps(totalPerps)
    writeTop50(PR)


    return 'finished'


def statReport(sources, sinks, totalNum):

    f = open("G1-stat.txt", "a") # report for statistic result of G1
#    f = open("G2-stat.txt", "a") # report for statistic result of G2
#    f = open("test-stat.txt", "a")  # report for statistic result of G1
    sourProp = len(sources) / float(totalNum)
    line = 'Sources proportion:' + '\n' + str(sourProp) + '\n\n'
    f.write(line)

    sinkProp =  len(sinks) / float(totalNum)
    line = 'Sinks proportion:' + '\n' + str(sinkProp) + '\n\n'
    f.write(line)

    line = 'Source Pages:' + '\n'
    f.write(line)

    for source in sources :
        line = source + '\n'
        f.write(line)

    line = '\n\n' + 'Sink Pages:' + '\n'
    f.write(line)
    for sink in sinks :
        line = sink + '\n'
        f.write(line)

    f.close()
    return

def writePerps(perps):

    for p in perps:
        line = str(p) + '\n'
        f = open("G1-perps.txt", "a") # write perplexities for G1
#        f = open("G2-perps.txt", "a")  # write perplexities for G2
#        f = open("test-perps.txt", "a") # write perplexities for G1
        f.write(line)
        f.close()

def writeTop50(PR):

    sortedPR = sorted(PR.iteritems(), key=lambda d: d[1], reverse=True)[:50]
    for item in sortedPR:
        line = str(item[0]) + ' ' + str(item[1]) + '\n'
        f = open("G1-PR.txt", "a") # write top50 pages for G1
#        f = open("G2-PR.txt", "a") # write top50 pages for G2
#        f = open("test-pr.txt", "a") # write top50 pages for G2
        f.write(line)
        f.close()


def getL(p):
    result = 0
    for e in eGraph:
        if e[0] == p: result +=1
    return result


def H(PG):
    value = 0
    PRs = PG.values()
    for rank in PRs:
        value += rank * math.log(rank, 2)
    return -value


def converge(perps): # check iff
    if len (perps) < 4 :
        return False
    else :
        difs = []
        for i in range(3):
            difs.append(perps[i + 1] - perps[i])
        converge = all(-1 < i < 1 for i in difs)
        if converge:
            return converge
        else:
            perps.pop(0)
        return converge


print  pageRank (0.85)






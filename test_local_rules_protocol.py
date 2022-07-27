import math
import random
import time
from queue import Queue
from threading import Thread, Event
from multiprocessing import Pool
import multiprocessing


def initialize_phase(n, gamma):
    result = {}
    result['m'] = n ** 3
    result['q'] = math.ceil(gamma * math.log(n))
    return result


def voting_intention_phase(i, m, n, q):
    for x in range(1, q + 1):
        v = random.randint(1, n)
        while v in H[i].keys():  # to avoid duplicates
            v = random.randint(1, n)
        rand2 = random.randint(1, n)
        H[i][v] = [random.randint(1, m), rand2]
        if rand2 not in appear:
            appear[rand2] = []
        appear[rand2].append({'H': H[i], 'u': i})
    if len(H[i]) != q:
        print("Error on voting intention phase")


def commitment_phase(i, q, n):
    for x in range(1, q + 1):
        h_i_keys = H[i].keys()
        v = random.choice(list(h_i_keys))
        while v in L[i].keys():
            v = random.randint(1, n)
        L[i][v] = {}
        for j in H[v].keys():
            L[i][v][j] = [v, H[v][j][0], H[v][j][1]]

        if len(L[i][v]) != len(H[v]):
            print("Error on commitment phase")
    # print(L[i])


def voting_phase(y, q, m):
    if y in appear:
        for v in appear[y]:
            print("APPEAR")
            print(v['u'])
            W[y][v['u']] = v['H']
    #for u in H.keys():
    #    for i in H[u].keys():
    #        if H[u][i][1] == y:
    #            W[y][u] = H[u]
    # ci devono essere tutti Wu con lunghezza q
    # while len(W[u]) < q:
    #    random_h = random.choice(list(H))
    #    while random_h in W[u]:
    #        random_h = random.choice(list(H))
    #    W[u][random_h] = H[random_h][u]
    # W[u][i] = H[i]

    k[y] = 0
    for key in W[y].keys():
        for key2 in W[y][key].keys():
            k[y] += W[y][key][key2][1]
    k[y] = k[y] % m
    print("Valore k per il nodo " + str(y) + ": " + str(k[y]))


def find_min_phase(u, q, n):
    CE[u] = [k[u], W[u], c[u], u]
    CE_min[u] = CE[u]
    choices = random.choices([i for i in range(1, n)], k=q)
    for i in choices:
        print(i)


def coherence_phase(q):
    for i in range(1, q + 1):
        # push CE_min to agent v u.a.r.
        if (2 > 1):
            print("FAIL!!!")
            return False
    CE_min = 3
    return True


def verification_phase():
    # if k_min = sum h in W_min h mod m and W_min consistent with L_u
    # support c_min
    # else fail
    return True


# A thread that consumes data
def consumer(i, n, gamma):
    print("ENTRO")
    phase = 'initialize'
    initialize = initialize_phase(n, gamma)
    m = initialize['m']
    q = initialize['q']
    voting_intention_phase(i, m, n, q)
    commitment_phase(i, q, n)
    # voting_phase(q)
    # find_min_phase(q)
    # coherence_phase(q)
    # verification_phase()


fails = 0
n = 100000
gamma = 0.8  # maximum number of faulty agents *
initialize = {}
appear = {}
m = {}
q = {}
H = {}
L = {}
W = {}
k = {}
CE = {}
CE_min = {}
c = {}
colors = ['green', 'red', 'blue', 'yellow', 'gray', 'black', 'white', 'emerald', 'pink', 'violet', 'amber', 'cyan']
for i in range(1, n + 1):
    H[i] = {}
    L[i] = {}
    W[i] = {}
    c[i] = colors[random.randint(0, len(colors) - 1)]

for i in range(1, n):
    initialize[i] = initialize_phase(n, gamma)
    m[i] = initialize[i]['m']
    q[i] = initialize[i]['q']

for i in range(1, n):
    voting_intention_phase(i, m[i], n, q[i])

for i in range(1, n):
    commitment_phase(i, q[i], n)

for i in range(1, n):
    voting_phase(i, q[i], m[i])

for u in range(1, n):
    CE[u] = [k[u], W[u], c[u], u]
    CE_min[u] = CE[u]

# find-min
for rounds in range(1, q[1] + 1):
    for u in range(1, n):
        v = random.choice([i for i in range(1, n)])
        if CE_min[v][0] < CE_min[u][0]:
            CE_min[u] = CE_min[v]

# coherence
for u in range(1, n):
    for rounds in range(1, q[1] + 1):
        v = random.choice([i for i in range(1, n)])
        if CE_min[u][3] != CE_min[v][3]:
            print("PROTOCOL FAIL!!")
            fails = fails + 1

for u in range(1, n):
    calcK = 0
    for key in CE_min[u][1].keys():
        for key2 in CE_min[u][1][key].keys():
            calcK += CE_min[u][1][key][key2][1]
    calcK = calcK % m[u]
    if calcK != CE_min[u][0]:
        print("PROTOCOL FAIL!")
    better_w = CE_min[u][1]
    for key in better_w.keys():
        #better_w[key] -> H_key, se ce l'ho allora faccio verifica
        if key in L[u].keys():
            for s in L[u][key].keys():
                for key2 in better_w[key].keys():
                    if L[u][key][s][2] == better_w[key][key2][1]:
                        if L[u][key][s][1] != better_w[key][key2][0]:
                            print("FAILZ")
                        else:
                            print("EQUAL!")



    # manca la parte del controllo di consistenza tra Wu e Lu

supported_colors = {}

for u in range(1, n):
    if CE_min[u][2] not in supported_colors:
        supported_colors[CE_min[u][2]] = 1
    else:
        supported_colors[CE_min[u][2]] = supported_colors[CE_min[u][2]] + 1

print("FAILS: " + str(fails))
for key in supported_colors.keys():
    print(key + ": " + str(supported_colors[key]))
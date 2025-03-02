import sys
import math


def readLine(line):
    values = line.split()
    rows = int(values[0])
    cols = int(values[1])

    matrix = []
    for i in range(rows):
        matrix.append([])
        for j in range(cols):
            matrix[i].append(float(values[i * cols + j + 2]))
    return matrix


def readLines():
    lines = sys.stdin.readlines()

    T = readLine(lines[0])
    O = readLine(lines[1])
    I = readLine(lines[2])

    line3 = lines[3].split()[1:]
    observations = []
    for i in range(len(line3)):
        observations.append(int(line3[i]))

    return T, O, I, observations


def abPass(alpha, beta, c, T, O, I, observations, N, tMax):
    # Alpha-Pass
    c[0] = 0
    for i in range(N):
        alpha[0][i] = O[i][observations[0]] * I[0][i]
        c[0] = c[0] + alpha[0][i]

    c[0] = 1 / c[0]
    for i in range(N):
        alpha[0][i] = c[0] * alpha[0][i]

    for t in range(1, tMax):
        c[t] = 0
        for i in range(N):
            alpha[t][i] = 0
            for j in range(N):
                alpha[t][i] = alpha[t][i] + alpha[t - 1][j] * T[j][i]
            alpha[t][i] = alpha[t][i] * O[i][observations[t]]
            c[t] = c[t] + alpha[t][i]
        c[t] = 1 / c[t]
        for i in range(N):
            alpha[t][i] = c[t] * alpha[t][i]

    # Beta-Pass
    for i in range(N):
        beta[tMax - 1][i] = c[tMax - 1]

    for t in range(tMax - 2, -1, -1):
        for i in range(N):
            beta[t][i] = 0
            for j in range(N):
                beta[t][i] = beta[t][i] + T[i][j] * O[j][observations[t + 1]] * beta[t + 1][j]
            beta[t][i] = c[t] * beta[t][i]


def computeGamma(gamma, diGamma, T, O, observations, alpha, beta, N, tMax):
    for t in range(tMax - 1):
        for i in range(N):
            gamma[t][i] = 0
            for j in range(N):
                diGamma[t][i][j] = alpha[t][i] * T[i][j] * O[j][observations[t + 1]] * beta[t + 1][j]
                gamma[t][i] = gamma[t][i] + diGamma[t][i][j]

    for i in range(N):
        gamma[tMax - 1][i] = alpha[tMax - 1][i]


def computeTOI(T, O, I, observations, gamma, diGamma, N, K, tMax):
    for i in range(N):
        I[0][i] = gamma[0][i]

    for i in range(N):
        denom = 0
        for t in range(tMax - 1):
            denom = denom + gamma[t][i]
        for j in range(N):
            numer = 0
            for t in range(tMax - 1):
                numer = numer + diGamma[t][i][j]
            T[i][j] = numer / denom

    for i in range(N):
        denom = 0
        for t in range(tMax):
            denom = denom + gamma[t][i]
        for j in range(K):
            numer = 0
            for t in range(tMax):
                if observations[t] == j:
                    numer = numer + gamma[t][i]
                O[i][j] = numer / denom


def computeLogProb(c, tMax):
    logProb = 0
    for i in range(tMax):
        logProb = logProb + math.log(c[i])
    return -logProb


def HMM3():
    T, O, I, observations = readLines()

    N = len(T)
    K = len(O[0])
    tMax = len(observations)

    c = [0] * tMax
    alpha = [[0] * N for _ in range(tMax)]
    beta = [[0] * N for _ in range(tMax)]
    gamma = [[0] * N for _ in range(tMax)]
    diGamma = [[[0] * N for _ in range(N)] for _ in range(tMax - 1)]

    oldLogProb = -float('inf')
    loopCount = 0
    while True:
        abPass(alpha, beta, c, T, O, I, observations, N, tMax)
        computeGamma(gamma, diGamma, T, O, observations, alpha, beta, N, tMax)
        computeTOI(T, O, I, observations, gamma, diGamma, N, K, tMax)

        logProb = computeLogProb(c, tMax)
        if logProb < oldLogProb:
            break
        oldLogProb = logProb

        loopCount += 1
        if loopCount > 42:
            break

    outT = f"{len(T)} {len(T[0])}"
    for i in range(N):
        for j in range(N):
            outT += f" {T[i][j]}"
    outO = f"{len(O)} {len(O[0])}"
    for j in range(N):
        for k in range(K):
            outO += f" {O[j][k]}"
    out = outT + "\n" + outO
    print(out)


HMM3()

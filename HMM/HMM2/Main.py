import sys


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


def HMM2Rec(T, O, I, observations):
    N = len(T)
    tMax = len(observations)

    delta = []
    deltaIdx = []
    for _ in range(tMax):
        delta.append([0] * N)
        deltaIdx.append([0] * N)

    # 2.16
    for i in range(N):
        delta[0][i] = O[i][observations[0]] * I[0][i]

    # 2.18
    for t in range(1, tMax):
        for i in range(N):
            maxValue = -1
            for j in range(N):
                currValue = T[j][i] * delta[t - 1][j]
                if maxValue < currValue:
                    maxValue = currValue
                    deltaIdx[t][i] = j
            delta[t][i] = O[i][observations[t]] * maxValue

    # 2.22
    result = [0] * tMax
    maxValue = -1
    for j in range(N):
        currValue = delta[tMax - 1][j]
        if maxValue < currValue:
            maxValue = currValue
            result[-1] = j
    for t in range(tMax - 2, -1, -1):
        result[t] = deltaIdx[t + 1][result[t + 1]]

    return result


def HMM2():
    T, O, I, observations = readLines()

    result = HMM2Rec(T, O, I, observations)
    out = f"{result[0]}"
    for i in range(1, len(result)):
        out += f" {result[i]}"
    print(out)


HMM2()

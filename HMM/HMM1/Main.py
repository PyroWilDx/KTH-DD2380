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


def HHM1Rec(T, O, I, observations):
    N = len(T)
    tMax = len(observations)

    alpha = []
    for _ in range(tMax):
        alpha.append([0] * N)

    # 2.6
    for i in range(N):
        alpha[0][i] = O[i][observations[0]] * I[0][i]

    # 2.9
    for t in range(1, tMax):
        for i in range(N):
            value = 0
            for j in range(N):
                value += T[j][i] * alpha[t - 1][j]
            alpha[t][i] = O[i][observations[t]] * value

    # 2.14
    result = 0
    for j in range(N):
        result += alpha[tMax - 1][j]

    return result


def HHM1():
    T, O, I, observations = readLines()

    result = HHM1Rec(T, O, I, observations)
    print(result)


HHM1()

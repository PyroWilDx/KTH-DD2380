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

    return T, O, I


def multMatrix(M1, M2):
    R = []
    for i in range(len(M1)):
        R.append([])
        for j in range(len(M2[0])):
            value = 0
            for k in range(len(M1[0])):
                value += M1[i][k] * M2[k][j]
            R[i].append(value)
    return R


def HMM0():
    T, O, I = readLines()

    E = multMatrix(multMatrix(I, T), O)

    out = f"{len(E)} {len(E[0])}"
    for v in E[0]:
        out += f" {v}"
    print(out)


HMM0()

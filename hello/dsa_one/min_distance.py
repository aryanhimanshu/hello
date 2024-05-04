def min_distance(points):
    if len(points) == 1:
        return 0
    if len(points) == 2:
        return abs(points[0][0] - points[1][0]) + abs(points[0][1] - points[1][1])
    points.sort()
    for i in range(0, len(points) - 2):
        points[i:i+3] =sortThree(points[i:i+3])
    distance = 0
    for i in range(0, len(points) - 1):
        distance += abs(points[i][0] - points[i + 1][0]) + abs(points[i][1] - points[i + 1][1])
    return distance

def sortThree(points):
    distance_1 = abs(points[0][0] - points[1][0]) + abs(points[0][1] - points[1][1])
    distance_2 = abs(points[1][0] - points[2][0]) + abs(points[1][1] - points[2][1])
    distance_3 = abs(points[0][0] - points[2][0]) + abs(points[0][1] - points[2][1])

    x1 = distance_1 + distance_2
    x2 = distance_1 + distance_3
    x3 = distance_2 + distance_3

    if x1 < x2 and x1 < x3:
        return [points[0], points[1], points[2]]
    if x2 < x1 and x2 < x3:
        if x1 < x3:
            return [points[0], points[1], points[2]]
        else:
            return [points[1], points[2], points[0]]
    if x3 < x1 and x3 < x2:
        return [points[0], points[2], points[1]]
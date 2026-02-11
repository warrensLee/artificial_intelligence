import numpy as np
import random
import math
from collections import deque
import heapq


class Geometry:
    count = 0

    def __init__(self, name="Shape", points=None):
        self.name = name
        # name is string that is a name of gemoetry
        self.points = points
        # points is a list of tuple points = [(x0, y0), (x1, y1), ...]
        Geometry.count += 1

    def calculate_area(self):
        return 0.0

    def get_name(self):
        return self.name

    @classmethod
    def count_number_of_geometry(cls):
        # TODO: Your task is to implement the class method
        # to get the number of instance that have already created
        return cls.count  # returns count of instances in that class


class Triangle(Geometry):
    def __init__(self, a, b, c):
        # a, b, c are tuples that represent for 3 vertices of a triangle
        # TODO: Your task is to implement the constructor
        super().__init__("Triangle", [a, b, c])
        # super(Triangle, self).__init__(a,b,c)

    def calculate_area(self):
        # TODO: Your task is required to implement a area function
        (x1, y1), (x2, y2), (x3, y3) = self.points
        return abs((x1*(y2-y3) + x2*(y3-y1) + x3*(y1-y2)) / 2)


class Rectangle(Geometry):
    def __init__(self, a, b):
        # a, b are tuples that represent for top and bottom vertices of a rectangle
        # TODO: Your task is to implement the constructor
        # super(Rectangle, self).__init__(a,b)
        super().__init__("Rectangle", [a, b])

    def calculate_area(self):
        # TODO: Your task is required to implement a area function
        (x1, y1), (x2, y2) = self.points
        length = abs(x2 - x1)
        width = abs(y2 - y1)
        return length * width


class Square(Rectangle):
    def __init__(self, a, length):
        # a is a tuple that represent a top vertex of a square
        # length is the side length of a square
        # TODO: Your task is to implement the constructor
        # super(Square, self).__init__(a, length)
        self.length = length
        b = (a[0] + length, a[1] + length)
        super().__init__(a, b)      # call Rectangle constructor
        self.name = "Square"        # overrides current name

    def calculate_area(self):
        # TODO: Your task is required to implement a area function
        return abs(self.length**2)


class Circle(Geometry):
    def __init__(self, o, r):
        # o is a tuple that represent a centre of a circle
        # r is the radius of a circle
        # TODO: Your task is to implement the constructor
        self.radius = r
        self.o = o
        # why not store radius too? Because points is for vertices only
        super().__init__("Circle", [o])

    def calculate_area(self):
        # TODO: Your task is required to implement a area function
        # pi r^2
        return math.pi * self.radius**2


class Polygon(Geometry):
    def __init__(self, points):
        # points is a list of tuples that represent vertices of a polygon
        # TODO: Your task is to implement the constructor
        # super(Polygon, self).__init__(?, ?)
        super().__init__("Polygon", points)

    def calculate_area(self):
        # TODO: Your task is required to implement a area function
        # Shoelace formula: Area = 1/2 * | Epsilon_i=0_n-1(x_i * y_i+1 - y_i * x_i+1) |
        n = len(self.points)
        area = 0.0
        for i in range(n):
            x1, y1 = self.points[i]
            # % n ensures that it wraps and checks first verticies again
            x2, y2 = self.points[(i + 1) % n]
            area = area + (x1 * y2) - (y1 * x2)

        return abs(area) * .5


def test_geomery():
    # Test cases for Problem 1

    triangle = Triangle((0, 1), (1, 0), (0, 0))
    print("Area of %s: %0.4f" % (triangle.name, triangle.calculate_area()))

    rectangle = Rectangle((0, 0), (2, 2))
    print("Area of %s: %0.4f" % (rectangle.name, rectangle.calculate_area()))

    square = Square((0, 0), 2)
    print("Area of %s: %0.4f" % (square.name, square.calculate_area()))

    circle = Circle((0, 0), 3)
    print("Area of %s: %0.4f" % (circle.name, circle.calculate_area()))

    polygon = Polygon([(0, 0), (0, 1), (1, 1), (1, 0)])
    print("Area of %s: %0.4f" % (polygon.name, polygon.calculate_area()))


def matrix_multiplication(A, B):
    # TODO: Your task is to required to implement
    # a matrix multiplication between A and B
    # A = (n, k) B = (k, m), and C = A x B => C = (n, m)
    n, k = A.shape
    k2, m = B.shape
    C = np.zeros((n, m))

    # check for size error
    if k != k2:
        print("Size error: The number of columns in A is not equal to the number of rows in B.")
        return None

    # loop thru each row in A
    for i in range(n):
        # loop thru each column in B
        for j in range(m):
            total = 0
            # loop thru inner dimensions that must match
            for p in range(k):
                total += A[i, p] * B[p, j]
            C[i, j] = total

    return C


def test_matrix_mul():
    ## Test cases for matrix multplication ##

    for test in range(10):
        m, n, k = random.randint(3, 10), random.randint(
            3, 10), random.randint(3, 10)
        A = np.random.randn(m, n)
        B = np.random.randn(n, k)
        assert np.mean(np.abs(A.dot(B) - matrix_multiplication(A, B))
                       ) <= 1e-7, "Your implmentation is wrong!"
        print("[Test Case %d]. Your implementation is correct!" % test)


def recursive_pow(A, n):
    # TODO: Your task is required implementing
    # a recursive function
    # base cases
    if n == 0:
        return np.eye(A.shape[0])  # returns identity matrix
    if n == 1:
        return A

    half = recursive_pow(A, n // 2)
    sq = matrix_multiplication(half, half)

    if n % 2 == 0:
        return sq
    else:
        return matrix_multiplication(A, sq)


def iterative_pow(A, n):
    # TODO: Your task is required implementing
    # a iterative function
    result = np.eye(A.shape[0])  # identity matrix
    base = A

    while n > 0:
        if n % 2 != 0:
            result = matrix_multiplication(result, base)
        base = matrix_multiplication(base, base)
        n //= 2

    return result


def test_pow():
    ## Test cases for the pow function ##
    for test in range(10):
        n = random.randint(2, 5)
        A = np.random.randn(n, n)
        print("Recursive: A^{} = {}".format(n, recursive_pow(A, n)))

    for test in range(10):
        n = random.randint(2, 5)
        A = np.random.randn(n, n)
        print("Iterative: A^{} = {}".format(n, iterative_pow(A, n)))


def get_A():
    # TODO: Find a matrix A
    # You have to return in the format of numpy array
    return np.array([[1.0, 1.0], [1.0, 0.0]])


def fibo(n):
    # TODO: Calcualte the n'th Fibonacci number
    if n <= 1:
        return 1

    A = get_A()  # fibb transition matrix

    F1 = np.array([[1.0], [1.0]]) # [f1, f0]^T
    P = recursive_pow(A, n - 1)  # get A^n-1

    Fn = matrix_multiplication(P, F1)
    return int(round(Fn[0,  0]))


def f(n, k):
    # TODO: Calcualte the n'th number of the recursive sequence
    if n < k:
        return 1

    A = np.zeros((k, k))
    A[0, :] = 1.0
    for i in range(1, k):
        A[i, i - 1] = 1.0

    S = np.ones((k, 1))

    P = recursive_pow(A, n - (k - 1))
    Sn = matrix_multiplication(P, S)

    return int(round(Sn[0, 0]))


def test_fibonacci():
    ## Test Cases for Fibonacci and Recursive Sequence ##
    a, b = 1, 1
    for i in range(2, 10):
        c = a + b
        assert (fibo(i) == c), "You implementation is incorrect"
        print("[Test Case %d]. Your implementation is correct!. fibo(%d) = %d" % (
            i - 2, i, fibo(i)))
        a = b
        b = c

    for n in range(5, 11):
        for k in range(2, 5):
            print("f(%d, %d) = %d" % (n, k, f(n, k)))


def DFS(A):
    # A is a mxn matrix
    m, n = A.shape
    # test cases where it is impossible due to a blocked start or goal
    if A[0, 0] == 0 or A[m - 1, n - 1] == 0:
        print(-1)  # Impossible because the start or end is blocked
        return

    # each cell visited will be stored as well as if we can traverse to it
    visited = np.zeros((m, n), dtype=bool)
    # row and column, followed by the path of decisions previoulsy made to allow us to back track and make a turn
    stack = [(0, 0, [(0, 0)])]
    # all possible decisions/directions: right, down, left, up
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    while stack:                            # while stack is not empty
        row, col, path = stack.pop()        # gets information necessary to complete

        if visited[row, col]:               # lets not work harder than we must
            continue

        visited[row, col] = True            # this cell has been visited now

        if row == m - 1 and col == n - 1:   # this is the cell we are looking for!
            print(" -> ".join(f"({x}, {y})" for x, y in path))
            return

        # try neighbors in fixed order: R, D, L, U
        for drow, dcol in directions:
            nrow, ncol = row + drow, col + dcol  # neighbor of said cell in each direction
            # if in bounds of matrix, a valid cell ( == 1), and has not been visited
            if (0 <= nrow < m and 0 <= ncol < n and A[nrow, ncol] == 1 and not visited[nrow, ncol]):
                # valid and unvisited cells gets added to the stack
                stack.append((nrow, ncol, path + [(nrow, ncol)]))

    print(-1)
    return


def BFS(A):
    # A is a mxn matrix
    m, n = A.shape
    # test cases where it is impossible due to a blocked start or goal
    if A[0, 0] == 0 or A[m - 1, n - 1] == 0:
        print(-1)  # Impossible because the start or end is blocked
        return

    # each cell visited will be stored as well as if we can traverse to it
    visited = np.zeros((m, n), dtype=bool)
    # to map the current (row,col) -> previous (row, col)
    parent = {}

    queue = deque()
    # adds (0, 0) init to the queue first to work as a starting point
    queue.append((0, 0))
    visited[0, 0] = True

    # all possible decisions/directions: right, down, left, up
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    while queue:                            # while queue is not empty
        row, col = queue.popleft()          # gets information necessary to complete

        if row == m - 1 and col == n - 1:   # this is the cell we are looking for!
            path = []
            current = (row, col)
            while current in parent:
                path.append(current)
                current = parent[current]
            path.append((0, 0))
            path.reverse()

            print(" -> ".join(f"({x}, {y})" for x, y in path))
            return

        # try neighbors in fixed order: R, D, L, U
        for drow, dcol in directions:
            nrow, ncol = row + drow, col + dcol  # neighbor of said cell in each direction
            # if in bounds of matrix, a valid cell ( == 1), and has not been visited
            if (0 <= nrow < m and 0 <= ncol < n and A[nrow, ncol] == 1 and not visited[nrow, ncol]):
                # valid and unvisited cells gets added to the queue
                visited[nrow, ncol] = True
                parent[(nrow, ncol)] = (row, col)
                queue.append((nrow, ncol))

    print(-1)
    return


def findMinimum(A):
    # A is a mxn matrix
    m, n = A.shape
    # test cases where it is impossible due to a blocked start or goal
    if A[0, 0] == 0 or A[m - 1, n - 1] == 0:
        print(-1)  # Impossible because the start or end is blocked
        return

    infinity = float("inf")
    distance = np.full((m, n), infinity)
    # to map the current (row,col) -> previous (row, col)
    parent = {}
    # start distance = 0 including A[0,0]
    distance[0, 0] = A[0, 0]

    # priority queue items: (total_cost (distance), row, column)
    priority_queue = [(A[0, 0], 0, 0)]

    # all possible decisions/directions: right, down, left, up
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    while priority_queue:                                       # while queue is not empty
        # gets information necessary to complete
        cost, row, col = heapq.heappop(priority_queue)

        # skip bad entries (we found a cheaper way already)
        if cost != distance[row, col]:
            continue

        if row == m - 1 and col == n - 1:                       # this is the cell we are looking for!
            path = []
            current = (row, col)
            while current in parent:
                # add cell to path and make current = to currents parent
                path.append(current)
                current = parent[current]
            # append this value
            path.append((0, 0))
            path.reverse()                                     # back track

            print(" -> ".join(f"({x}, {y})" for x, y in path))
            print("Total value: {}".format(int(distance[row, col])))
            return

        # try neighbors in fixed order: R, D, L, U
        for drow, dcol in directions:
            nrow, ncol = row + drow, col + dcol  # neighbor of said cell in each direction
            # if in bounds of matrix, a valid cell ( == 1), and has not been visited
            if (0 <= nrow < m and 0 <= ncol < n and A[nrow, ncol] != 0):
                # increment cost so it is valid
                new_cost = cost + A[nrow, ncol]

                if new_cost < distance[nrow, ncol]:
                    distance[nrow, ncol] = new_cost
                    parent[(nrow, ncol)] = (row, col)
                    heapq.heappush(priority_queue, (new_cost, nrow, ncol))

    print(-1)
    return


def test_bfs_dfs_find_minimum():
    ## Test Cases for BFS, DFS, Find Minimum ##
    A = np.array([[1, 1, 1, 0, 1], [0, 0, 1, 0, 0], [
                 1, 1, 1, 1, 1], [1, 1, 0, 1, 1], [1, 1, 0, 1, 1]])

    BFS(A)

    DFS(A)

    A = np.array([[1, 1, 1, 0, 1], [0, 0, 1, 0, 0], [
                 1, 1, 1, 1, 2], [1, 1, 0, 2, 1], [1, 1, 0, 2, 1]])

    findMinimum(A)

# Testing Your Code


test_geomery()
test_matrix_mul()
test_pow()
test_fibonacci()
test_bfs_dfs_find_minimum()

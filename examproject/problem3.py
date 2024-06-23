import numpy as np
import matplotlib.pyplot as plt

def question1():
    """
    Generates random points in a unit square and finds points A, B, C, D that form two triangles around a random point y.
    Plots the points and the triangles.

    Returns:
        The random point y, and the points A, B, C, D.
    """
    # Random points in the unit square
    rng = np.random.default_rng(2024)
    X = rng.uniform(size=(50, 2))
    y = rng.uniform(size=(2,))

    # Function to calculate distance
    def distance(p1, p2):
        return np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

    # Finding points A, B, C, D
    A = min([point for point in X if point[0] > y[0] and point[1] > y[1]], key=lambda point: distance(point, y))
    B = min([point for point in X if point[0] > y[0] and point[1] < y[1]], key=lambda point: distance(point, y))
    C = min([point for point in X if point[0] < y[0] and point[1] < y[1]], key=lambda point: distance(point, y))
    D = min([point for point in X if point[0] < y[0] and point[1] > y[1]], key=lambda point: distance(point, y))

    # Plotting the points and triangles
    plt.figure(figsize=(8, 8))
    plt.scatter(X[:, 0], X[:, 1], label='Random Points')
    plt.scatter([y[0]], [y[1]], color='red', label='y')
    plt.scatter([A[0], B[0], C[0], D[0]], [A[1], B[1], C[1], D[1]], color='green', label='A, B, C, D')

    # Draw triangles
    triangle_ABC = plt.Polygon([A, B, C], fill=None, edgecolor='blue', label='Triangle ABC')
    triangle_CDA = plt.Polygon([C, D, A], fill=None, edgecolor='purple', label='Triangle CDA')
    plt.gca().add_patch(triangle_ABC)
    plt.gca().add_patch(triangle_CDA)

    plt.xlabel('x1')
    plt.ylabel('x2')
    plt.legend()
    plt.title('Points and Triangles')
    plt.grid(True)
    plt.show()

    return y, A, B, C, D

def question2():
    """
    Generates random points in a unit square and finds points A, B, C, D that form two triangles around a random point y.
    Computes the barycentric coordinates of y with respect to the triangles and checks if y is inside either triangle.

    Returns:
        The random point y, the points A, B, C, D, the barycentric coordinates with respect to triangles ABC and CDA,
               and booleans indicating if y is inside the triangles.
    """
    # Random points in the unit square
    rng = np.random.default_rng(2024)
    X = rng.uniform(size=(50, 2))
    y = rng.uniform(size=(2,))

    # Function to calculate distance
    def distance(p1, p2):
        return np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

    # Finding points A, B, C, D
    A = min([point for point in X if point[0] > y[0] and point[1] > y[1]], key=lambda point: distance(point, y))
    B = min([point for point in X if point[0] > y[0] and point[1] < y[1]], key=lambda point: distance(point, y))
    C = min([point for point in X if point[0] < y[0] and point[1] < y[1]], key=lambda point: distance(point, y))
    D = min([point for point in X if point[0] < y[0] and point[1] > y[1]], key=lambda point: distance(point, y))

    # Function to compute barycentric coordinates
    def barycentric_coords(x, y, z, p):
        denom = (y[1] - z[1]) * (x[0] - z[0]) + (z[0] - y[0]) * (x[1] - z[1])
        a = ((y[1] - z[1]) * (p[0] - z[0]) + (z[0] - y[0]) * (p[1] - z[1])) / denom
        b = ((z[1] - x[1]) * (p[0] - z[0]) + (x[0] - z[0]) * (p[1] - z[1])) / denom
        c = 1 - a - b
        return a, b, c

    # Compute barycentric coordinates for triangles ABC and CDA
    r_ABC = barycentric_coords(A, B, C, y)
    r_CDA = barycentric_coords(C, D, A, y)

    # Check if point y is inside the triangle using barycentric coordinates
    def is_inside_triangle(r):
        return all(0 <= coord <= 1 for coord in r)

    inside_ABC = is_inside_triangle(r_ABC)
    inside_CDA = is_inside_triangle(r_CDA)

    return y, A, B, C, D, r_ABC, r_CDA, inside_ABC, inside_CDA

def question3():
    """
    Generates random points in a unit square and finds points A, B, C, D that form two triangles around a random point y.
    Computes the barycentric coordinates of y with respect to the triangles, checks if y is inside either triangle, and
    interpolates the value of f(y) using the barycentric coordinates. Compares the interpolated value with the true value of f(y).

    Returns:
        The random point y, the interpolated value of f(y), and the true value of f(y).
    """
    # Random points in the unit square
    rng = np.random.default_rng(2024)
    X = rng.uniform(size=(50, 2))
    y = rng.uniform(size=(2,))

    # Define the function f
    f = lambda x: x[0] * x[1]
    F = np.array([f(x) for x in X])

    # Function to calculate distance
    def distance(p1, p2):
        return np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

    # Finding points A, B, C, D
    A = min([point for point in X if point[0] > y[0] and point[1] > y[1]], key=lambda point: distance(point, y))
    B = min([point for point in X if point[0] > y[0] and point[1] < y[1]], key=lambda point: distance(point, y))
    C = min([point for point in X if point[0] < y[0] and point[1] < y[1]], key=lambda point: distance(point, y))
    D = min([point for point in X if point[0] < y[0] and point[1] > y[1]], key=lambda point: distance(point, y))

    # Function to compute barycentric coordinates
    def barycentric_coords(x, y, z, p):
        denom = (y[1] - z[1]) * (x[0] - z[0]) + (z[0] - y[0]) * (x[1] - z[1])
        a = ((y[1] - z[1]) * (p[0] - z[0]) + (z[0] - y[0]) * (p[1] - z[1])) / denom
        b = ((z[1] - x[1]) * (p[0] - z[0]) + (x[0] - z[0]) * (p[1] - z[1])) / denom
        c = 1 - a - b
        return a, b, c

    # Compute barycentric coordinates for triangles ABC and CDA
    r_ABC = barycentric_coords(A, B, C, y)
    r_CDA = barycentric_coords(C, D, A, y)

    # Check if point y is inside the triangle using barycentric coordinates
    def is_inside_triangle(r):
        return all(0 <= coord <= 1 for coord in r)

    inside_ABC = is_inside_triangle(r_ABC)
    inside_CDA = is_inside_triangle(r_CDA)

    # Function to interpolate using barycentric coordinates
    def interpolate(f_vals, bary_coords):
        return sum(f_val * bary_coord for f_val, bary_coord in zip(f_vals, bary_coords))

    # Interpolate the value of f(y)
    if inside_ABC:
        f_y_approx = interpolate([f(A), f(B), f(C)], r_ABC)
    elif inside_CDA:
        f_y_approx = interpolate([f(C), f(D), f(A)], r_CDA)
    else:
        f_y_approx = np.nan

    # True value of f(y)
    f_y_true = f(y)

    return y, f_y_approx, f_y_true

def question4():
    """
    Generates random points in a unit square and processes a list of fixed points y_points. For each point y in y_points,
    finds points A, B, C, D that form two triangles around y, computes the barycentric coordinates of y with respect to the triangles,
    checks if y is inside either triangle, interpolates the value of f(y) using the barycentric coordinates, and compares the interpolated
    value with the true value of f(y). Plots the points and the triangles for the last point in y_points.

    Returns:
        None
    """
    # Random points in the unit square
    rng = np.random.default_rng(2024)
    X = rng.uniform(size=(50, 2))
    y_points = [(0.2, 0.2), (0.8, 0.2), (0.8, 0.8), (0.5, 0.5)]

    # Define the function f
    f = lambda x: x[0] * x[1]
    F = np.array([f(x) for x in X])

    # Function to calculate distance
    def distance(p1, p2):
        return np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

    # Function to find the points A, B, C, D
    def find_points(y):
        candidates_A = [point for point in X if point[0] > y[0] and point[1] > y[1]]
        candidates_B = [point for point in X if point[0] > y[0] and point[1] < y[1]]
        candidates_C = [point for point in X if point[0] < y[0] and point[1] < y[1]]
        candidates_D = [point for point in X if point[0] < y[0] and point[1] > y[1]]

        A = min(candidates_A, key=lambda point: distance(point, y)) if candidates_A else None
        B = min(candidates_B, key=lambda point: distance(point, y)) if candidates_B else None
        C = min(candidates_C, key=lambda point: distance(point, y)) if candidates_C else None
        D = min(candidates_D, key=lambda point: distance(point, y)) if candidates_D else None

        return A, B, C, D

    # Function to compute barycentric coordinates
    def barycentric_coords(x, y, z, p):
        denom = (y[1] - z[1]) * (x[0] - z[0]) + (z[0] - y[0]) * (x[1] - z[1])
        a = ((y[1] - z[1]) * (p[0] - z[0]) + (z[0] - y[0]) * (p[1] - z[1])) / denom
        b = ((z[1] - x[1]) * (p[0] - z[0]) + (x[0] - z[0]) * (p[1] - z[1])) / denom
        c = 1 - a - b
        return a, b, c

    # Check if point y is inside the triangle using barycentric coordinates
    def is_inside_triangle(r):
        return all(0 <= coord <= 1 for coord in r)

    # Function to interpolate using barycentric coordinates
    def interpolate(f_vals, bary_coords):
        return sum(f_val * bary_coord for f_val, bary_coord in zip(f_vals, bary_coords))

    # Process each point in y_points
    results = []

    for y in y_points:
        A, B, C, D = find_points(y)

        if A is None or B is None or C is None or D is None:
            f_y_approx = np.nan
        else:
            r_ABC = barycentric_coords(A, B, C, y)
            r_CDA = barycentric_coords(C, D, A, y)

            inside_ABC = is_inside_triangle(r_ABC)
            inside_CDA = is_inside_triangle(r_CDA)

            if inside_ABC:
                f_y_approx = interpolate([f(A), f(B), f(C)], r_ABC)
            elif inside_CDA:
                f_y_approx = interpolate([f(C), f(D), f(A)], r_CDA)
            else:
                f_y_approx = np.nan

        f_y_true = f(y)
        results.append((y, f_y_approx, f_y_true))

    # Plotting the points and triangles for the last y in y_points
    plt.figure(figsize=(8, 8))
    plt.scatter(X[:, 0], X[:, 1], label='Random Points')
    for y in y_points:
        plt.scatter([y[0]], [y[1]], color='red', label=f'y={y}')
    A, B, C, D = find_points(y_points[-1])
    if A is not None and B is not None and C is not None and D is not None:
        plt.scatter([A[0], B[0], C[0], D[0]], [A[1], B[1], C[1], D[1]], color='green', label='A, B, C, D')
        # Draw triangles
        triangle_ABC = plt.Polygon([A, B, C], fill=None, edgecolor='blue', label='Triangle ABC')
        triangle_CDA = plt.Polygon([C, D, A], fill=None, edgecolor='purple', label='Triangle CDA')
        plt.gca().add_patch(triangle_ABC)
        plt.gca().add_patch(triangle_CDA)

    plt.xlabel('x1')
    plt.ylabel('x2')
    plt.legend()
    plt.title('Points and Triangles')
    plt.grid(True)
    plt.show()

    # Print results
    for y, f_y_approx, f_y_true in results:
        print(f"Point y: {y}")
        print(f"Approximated value of f(y): {f_y_approx}")
        print(f"True value of f(y): {f_y_true}")
        print("---")

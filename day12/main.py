import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../utils'))

from utils import get_input_filename, read_input_file

def fill_plot(type, i, j, region, data, n_rows, n_cols):
    if i >= 0 and i < n_rows and j >= 0 and j < n_cols and data[i][j] == type and (i,j) not in region:
        region.append((i,j))
        fill_plot(type, i+1, j, region, data, n_rows, n_cols)
        fill_plot(type, i-1, j, region, data, n_rows, n_cols)
        fill_plot(type, i, j+1, region, data, n_rows, n_cols)
        fill_plot(type, i, j-1, region, data, n_rows, n_cols)

def compute_area_perimeter(region):
    i_min = min([i for i, j in region])
    i_max = max([i for i, j in region])
    j_min = min([j for i, j in region])
    j_max = max([j for i, j in region])

    n_rows = i_max - i_min + 1
    n_cols = j_max - j_min + 1
    field = [[0 for _ in range(n_cols + 2)] for _ in range(n_rows + 2)]
    area = 0
    for pos in region:
        field[pos[0] - i_min + 1][pos[1] - j_min + 1] = 1
        area += 1

    if verbose:
        for i in range(len(field)):
            print(field[i])

    perimeter = 0
    for i in range(len(field)):
        for j in range(len(field[0]) - 1):
            if field[i][j] != field[i][j+1]:
                perimeter += 1

    for i in range(len(field) - 1):
        for j in range(len(field[0])):
            if field[i][j] != field[i+1][j]:
                perimeter += 1

    return area, perimeter

def compute_area_sides(region):
    i_min = min([i for i, j in region])
    i_max = max([i for i, j in region])
    j_min = min([j for i, j in region])
    j_max = max([j for i, j in region])

    n_rows = i_max - i_min + 1
    n_cols = j_max - j_min + 1
    field = [[0 for _ in range(n_cols + 2)] for _ in range(n_rows + 2)]
    area = 0
    for pos in region:
        field[pos[0] - i_min + 1][pos[1] - j_min + 1] = 1
        area += 1

    if verbose:
        for i in range(len(field)):
            print(field[i])

    # Find all edges
    edge_list = []
    for i in range(len(field)):
        for j in range(len(field[0]) - 1):
            if field[i][j] != field[i][j+1]:
                edge_list.append(((i,j+1), (i+1,j+1), "v"))

    for i in range(len(field) - 1):
        for j in range(len(field[0])):
            if field[i][j] != field[i+1][j]:
                edge_list.append(((i+1,j), (i+1,j+1), "h"))

    # Find all contours of the region
    sides = 0
    contour_nodes = []
    valid_edges = [True for _ in range(len(edge_list))]
    contour_nodes.append(edge_list[0][0])
    contour_nodes.append(edge_list[0][1])
    orientation = edge_list[0][2]
    valid_edges[0] = False
    num_edge_per_node = {}
    for x1, x2, edge_orientation in edge_list:
        if x1 not in num_edge_per_node:
            num_edge_per_node[x1] = 0
        if x2 not in num_edge_per_node:
            num_edge_per_node[x2] = 0

        num_edge_per_node[x1] += 1
        num_edge_per_node[x2] += 1
    while sum(valid_edges) > 0:
        for iedge, (x1, x2, edge_orientation) in enumerate(edge_list):
            if not valid_edges[iedge]:
                continue

            if x2 == contour_nodes[-1]:
                x1, x2 = x2, x1

            if x1 == contour_nodes[-1]:
                # If the point is an intersction, force it to be a corner
                if num_edge_per_node[x1] > 2 and edge_orientation == orientation:
                    continue

                valid_edges[iedge] = False
                if edge_orientation == orientation:
                    contour_nodes[-1] = x2
                else:
                    contour_nodes.append(x2)
                    orientation = edge_orientation

                break

        if contour_nodes[0] == contour_nodes[-1]:
            sides += len(contour_nodes) - 1
            contour_nodes = []
            if sum(valid_edges) > 0:
                for iedge in range(len(edge_list)):
                    if valid_edges[iedge]:
                        break

                contour_nodes.append(edge_list[iedge][0])
                contour_nodes.append(edge_list[iedge][1])
                orientation = edge_list[iedge][2]
                valid_edges[iedge] = False

    return area, sides


if __name__ == '__main__':
    filename, part = get_input_filename(os.path.dirname(__file__))
    data = read_input_file(filename)[0]

    n_rows = len(data)
    n_cols = len(data[0])

    verbose = False

    if part == '1':
        result1 = 0
        visited = [[False for _ in range(n_cols)] for _ in range(n_rows)]
        for i in range(n_rows):
            for j in range(n_cols):
                if not visited[i][j]:
                    region = []
                    fill_plot(data[i][j], i, j, region, data, n_rows, n_cols)
                    area, perimeter = compute_area_perimeter(region)
                    result1 += area * perimeter
                    for x, y in region:
                        visited[x][y] = True

        print("Result of part 1: ", result1)

    elif part == '2':
        result2 = 0
        visited = [[False for _ in range(n_cols)] for _ in range(n_rows)]
        for i in range(n_rows):
            for j in range(n_cols):
                if not visited[i][j]:
                    region = []
                    fill_plot(data[i][j], i, j, region, data, n_rows, n_cols)
                    area, sides = compute_area_sides(region)
                    result2 += area * sides
                    for x, y in region:
                        visited[x][y] = True

        print("Result of part 2: ", result2)
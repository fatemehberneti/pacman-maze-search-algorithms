import matplotlib.pyplot as plt
from tree_algorithms import *
import time

# Set up a 1x2 grid for the subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Data for number of nodes explored plot (left plot)
num_mazes_range = range(1, 11)

# Measure the number of nodes explored for each algorithm
def measure_nodes_explored(algorithm, start, goal, maze):
    path, nodes = algorithm(start, goal, maze)
    return nodes

# Compare the algorithms for 1 to 10 mazes
bfs_nodes = []
dfs_nodes = []
ids_nodes = []
aStar_manhattan_nodes = []
aStar_eculidean_nodes = []

for num_mazes in range(1, 11):  # Run for 1 to 10 mazes
    bfs_total_nodes = 0
    dfs_total_nodes = 0
    ids_total_nodes = 0
    aStar_manhattan_total_nodes = 0
    aStar_euclidean_total_nodes = 0

    for _ in range(num_mazes):
        maze = generate_maze(ROWS, COLS)

        # Measure number of nodes for each algorithm
        bfs_total_nodes += measure_nodes_explored(bfs_tree, start, goal, maze)
        dfs_total_nodes += measure_nodes_explored(dfs_tree, start, goal, maze)
        ids_total_nodes += measure_nodes_explored(ids_tree, start, goal, maze)
        aStar_manhattan_total_nodes += measure_nodes_explored(a_star_tree_manhattan, start, goal, maze)
        aStar_euclidean_total_nodes += measure_nodes_explored(a_star_tree_euclidean, start, goal, maze)

    # Calculate average number of nodes explored
    bfs_nodes.append(bfs_total_nodes / num_mazes)
    dfs_nodes.append(dfs_total_nodes / num_mazes)
    ids_nodes.append(ids_total_nodes / num_mazes)
    aStar_manhattan_nodes.append(aStar_manhattan_total_nodes / num_mazes)
    aStar_eculidean_nodes.append(aStar_euclidean_total_nodes / num_mazes)

# Plot the number of nodes explored
ax1.plot(num_mazes_range, bfs_nodes, label='BFS', color='blue', marker='o')
ax1.plot(num_mazes_range, dfs_nodes, label='DFS', color='green', marker='o')
ax1.plot(num_mazes_range, ids_nodes, label='IDS', color='red', marker='o')
ax1.plot(num_mazes_range, aStar_manhattan_nodes, label='A* (manhattan)', color='orange', marker='o')
ax1.plot(num_mazes_range, aStar_eculidean_nodes, label='A* (eculidean)', color='purple', marker='o')
ax1.set_xlabel('Number of Mazes')
ax1.set_ylabel('Average Nodes Explored')
ax1.set_title('Algorithm Comparison by Nodes Explored as Number of Mazes Increases')
ax1.legend()
ax1.grid(True)

# Data for runtime comparison plot (right plot)

# Measure the runtime of each algorithm
def measure_runtime(algorithm, start, goal, maze):
    start_time = time.time()
    algorithm(start, goal, maze)
    end_time = time.time()
    return end_time - start_time

# Compare the algorithms for 1 to 10 mazes
bfs_final = []
dfs_final = []
ids_final = []
aStar_manhattan_final = []
aStar_eculidean_final = []

for num_mazes in range(1, 11):  # Run for 1 to 10 mazes
    bfs_total_time = 0
    dfs_total_time = 0
    ids_total_time = 0
    aStar_manhattan_total_time = 0
    aStar_euclidean_total_time = 0

    for _ in range(num_mazes):
        maze = generate_maze(ROWS, COLS)

        # Measure time for each algorithm
        bfs_total_time += measure_runtime(bfs_tree, start, goal, maze)
        dfs_total_time += measure_runtime(dfs_tree, start, goal, maze)
        ids_total_time += measure_runtime(ids_tree, start, goal, maze)
        aStar_manhattan_total_time += measure_runtime(a_star_tree_manhattan, start, goal, maze)
        aStar_euclidean_total_time += measure_runtime(a_star_tree_euclidean, start, goal, maze)

    # Calculate average time
    bfs_final.append(bfs_total_time / num_mazes)
    dfs_final.append(dfs_total_time / num_mazes)
    ids_final.append(ids_total_time / num_mazes)
    aStar_manhattan_final.append(aStar_manhattan_total_time / num_mazes)
    aStar_eculidean_final.append(aStar_euclidean_total_time / num_mazes)

# Plot the runtime comparison
ax2.plot(num_mazes_range, bfs_final, label='BFS', color='blue', marker='o')
ax2.plot(num_mazes_range, dfs_final, label='DFS', color='green', marker='o')
ax2.plot(num_mazes_range, ids_final, label='IDS', color='red', marker='o')
ax2.plot(num_mazes_range, aStar_manhattan_final, label='A* (manhattan)', color='orange', marker='o')
ax2.plot(num_mazes_range, aStar_eculidean_final, label='A* (eculidean)', color='purple', marker='o')
ax2.set_xlabel('Number of Mazes')
ax2.set_ylabel('Average Time (seconds)')
ax2.set_title('Algorithm Comparison by Time as Number of Mazes Increases')
ax2.legend()
ax2.grid(True)

# Adjust layout and display both plots
plt.tight_layout()
plt.savefig("tree_search_benchmark.png", dpi=300, bbox_inches="tight")
plt.show()

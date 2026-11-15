# Pac-Man & Maze AI Search Algorithms

A Python implementation and empirical comparison of classical **Artificial Intelligence Search & Pathfinding Algorithms** across both **Graph Search** and **Tree Search** paradigms[cite: 5, 8, 9, 12, 16]. This project features procedural maze generation (Prim's Algorithm & randomized grids)[cite: 5, 12], interactive **Pygame** visualizations[cite: 8, 12, 16], a playable **Pac-Man** pathfinding demo, and **Matplotlib** benchmarks comparing execution time and explored node counts[cite: 13, 14].

## Features

* **Uninformed & Informed Search Algorithms:**
  * **Graph Search (`graph_algorithms.py`, `visualizer_graph.py`):** Breadth-First Search (**BFS**), Depth-First Search (**DFS**), and Iterative Deepening Search (**IDS**) utilizing a `visited` set and a custom linked-list **Queue** (`my_queue.py`) to prevent cycles[cite: 5, 6, 10, 16].
  * **Tree Search & Heuristics (`tree_algorithms.py`, `visualizer_tree_astar.py`):** Tree-based **BFS**, **DFS**, **IDS**, and **A\*** Search implemented with both **Manhattan** and **Euclidean** distance heuristics using priority queues (`heapq`)[cite: 9, 12].
* **Interactive Pygame Visualizers:**
  * **Tree Search & A\* Visualizer (`visualizer_tree_astar.py`):** Animates step-by-step node exploration (blue) and optimal path reconstruction (orange) sequentially across BFS, DFS, IDS, A\* (Manhattan), and A\* (Euclidean)[cite: 12].
  * **Graph Maze Visualizer (`visualizer_graph.py`):** Generates cycle-free mazes via **Prim's Algorithm** and animates pathfinding from start to goal[cite: 16].
  * **Interactive Pac-Man Demo (`pacman_game.py`):** Playable Pac-Man grid game where you control Pac-Man with arrow keys while the chosen search algorithm dynamically highlights the shortest path to spawning food[cite: 8].
* **Performance Benchmarks & Analysis (`benchmark_tree.py`, `benchmark_graph.py`, `experiments_notebook.ipynb`):**
  * Evaluates algorithm scalability across increasing numbers of generated mazes (1 to 10 mazes)[cite: 13, 14].
  * Generates side-by-side comparison plots for **Average Nodes Explored** and **Average Execution Time (seconds)**[cite: 13, 14].

## Requirements

* **Python:** 3.8 – 3.14+
* **Libraries:**
  * `pygame` (for Python 3.8 – 3.13) **or** `pygame-ce` (recommended for Python 3.14+ / Apple Silicon)[cite: 8, 12, 16]
  * `matplotlib` (for generating runtime and node-exploration benchmark plots)[cite: 13, 14]
  * `jupyter` / `notebook` (optional, to view `experiments_notebook.ipynb`)[cite: 15]

## Project Structure

```text
├── my_queue.py                  # Custom linked-list Node & Queue data structure[cite: 6]
├── pacman_game.py               # Interactive Pygame Pac-Man game with live pathfinding[cite: 8]
├── visualizer_graph.py          # Prim's maze generator & Graph Search Pygame visualizer[cite: 16]
├── visualizer_tree_astar.py     # Tree Search & A* (Manhattan/Euclidean) Pygame visualizer[cite: 12]
├── graph_algorithms.py          # Graph Search algorithms instrumented for node & time benchmarks[cite: 5, 10]
├── tree_algorithms.py           # Tree Search & A* implementations for benchmarking[cite: 9]
├── benchmark_graph.py           # Multi-maze scalability plots (Nodes & Time) for Graph Search[cite: 14]
├── benchmark_tree.py            # Multi-maze scalability plots (Nodes & Time) for Tree Search & A*[cite: 13]
├── experiments_notebook.ipynb   # Jupyter Notebook documenting experimental outputs & plots[cite: 15]
├── tree_search_benchmark.jpg    # Benchmark chart for Tree Search & A*[cite: 17]
├── graph_search_benchmark.jpg   # Benchmark chart for Graph Search[cite: 18]
└── README.md

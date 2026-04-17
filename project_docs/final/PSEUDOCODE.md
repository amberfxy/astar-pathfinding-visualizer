# CS5800 Final Project Pseudocode

## Search Framework

```text
function SearchGenerator(grid, heuristic):
    start <- grid.start
    goal <- grid.goal

    g[start] <- 0
    f[start] <- heuristic(start, goal)
    came_from[start] <- NIL

    open_heap <- min-heap containing (f[start], 0, start)
    open_set <- {start}
    closed <- {}
    counter <- 0

    while open_heap is not empty:
        (_, _, current) <- pop_min(open_heap)

        if current is in closed:
            continue

        remove current from open_set
        add current to closed

        yield state_snapshot(
            expanded=closed,
            frontier=open_set,
            current=current,
            g_values=g,
            f_values=f
        )

        if current = goal:
            path <- reconstruct_path(came_from, goal)
            return final_state(
                path=path,
                path_cost=g[goal],
                found=True
            )

        for each neighbor in walkable_4_neighbors(current):
            if neighbor is in closed:
                continue

            tentative_g <- g[current] + cost_to_enter(neighbor)

            if tentative_g < g.get(neighbor, infinity):
                g[neighbor] <- tentative_g
                came_from[neighbor] <- current
                f[neighbor] <- tentative_g + heuristic(neighbor, goal)

                counter <- counter + 1
                push(open_heap, (f[neighbor], counter, neighbor))
                add neighbor to open_set

    return final_state(path=[], found=False)
```

## Path Reconstruction

```text
function ReconstructPath(came_from, goal):
    path <- []
    current <- goal

    while current is not NIL:
        prepend current to path
        current <- came_from[current]

    return path
```

## Heuristics

```text
function ZeroHeuristic(node, goal):
    return 0

function ManhattanHeuristic(node, goal):
    return abs(node.row - goal.row) + abs(node.col - goal.col)

function EuclideanHeuristic(node, goal):
    return sqrt((node.row - goal.row)^2 + (node.col - goal.col)^2)
```

## Algorithm Modes

```text
Dijkstra(grid) = SearchGenerator(grid, ZeroHeuristic)
AStarManhattan(grid) = SearchGenerator(grid, ManhattanHeuristic)
AStarEuclidean(grid) = SearchGenerator(grid, EuclideanHeuristic)
```

## Complexity

- Time complexity: approximately `O(|E| + |V| log |V|)` with a min-heap frontier
- Space complexity: `O(|V|)` for the heap, score maps, closed set, and predecessor map

## Notes

- The grid is weighted and 4-directional.
- Correctness should be evaluated primarily by `path cost`, not only by `path length`.
- Dijkstra is included as the uninformed baseline by setting `h(n) = 0`.

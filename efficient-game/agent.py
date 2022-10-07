from copy import deepcopy
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import constants
import os 


class Agent:

    def __init__(self):
        self.location = (0, 0)
        self.is_alive = True

    def get_valid_neighbors(self, pos, grid):
        """
        gets all valid neighbors in-bound
        and they are not blocked by path
        specify WHICH GRID:
        - self.maze_grid
        - self.effective_maze 
        """
        x, y = pos[0], pos[1]

        left = (x-1, y) if x > 0 else None
        right = (x+1, y) if x < constants.SIZE[0]-1 else None
        up = (x, y-1) if y > 0 else None
        down = (x, y+1) if y < constants.SIZE[1]-1 else None

        return list(filter(lambda x: x != None and grid[x[0]][x[1]] == 0, [left, right, up, down]))

    def bfs(self, env, goal, queue, visited, prev):
        """
        runs BFS on grid and stores prev pointers to restore path.
        """
        while len(queue) > 0:
            # print(queue)
            parent = queue.pop(0)
            visited.add(parent)
            if parent == goal:
                return prev
            neighbors = self.get_valid_neighbors(parent, env.maze_grid)
            for neighbor in neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    prev[neighbor] = parent
        return prev

    def path_from_pointers(self, source, goal, prev):
        """
        returns solution path from start to end node
        """
        path = [goal]
        current = goal
        while current != source:
            path.append(prev[current])
            current = prev[current]
        return list(reversed(path))

    def plan_path(self, env, source=(0, 0)):
        """
        plans path agent will to get to end from source.
        """
        # use queue/visited/prev for running BFS for path planning
        queue = [source]
        visited = set(source)
        prev = ({source: None})

        # run BFS to find optimal path from start to end without ghosts
        previous = self.bfs(env, (constants.SIZE[0]-1, constants.SIZE[1]-1), queue, visited, prev)

        # finds optimal path from the BFS having stored prev pointers
        path = self.path_from_pointers(source, (constants.SIZE[0]-1, constants.SIZE[1]-1), previous)

        # returns the optimal path from source to destination
        return path

    def manhattan_distance(self, coord1, coord2):
        """
        calculates manhattan distance between two coordinates
        """
        x = abs(coord2[0] - coord1[0])
        y = abs(coord2[1] - coord1[1])
        return x + y

    def get_image_array(self, env):
        """
        0: unblocked cell
        1: blocked cell
        2: cell with ghost
        3: agent location 
        """
        color_array = deepcopy(env.maze_grid)
        color_array[env.ghost_grid == 1] = 2
        color_array[self.location[0]][self.location[1]] = 3
        return color_array

    def generate_video(self, video_name, images):
        """
        generates video of agent's moves
        """
        frames = []
        fig = plt.figure()
        for i in range(len(images)):
            frames.append([plt.imshow(images[i], cmap='Greys', animated=True)])

        plt.close()

        ani = animation.ArtistAnimation(
            fig, frames, interval=120, blit=True, repeat=False)

        path="replays/"
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
        
        ani.save("./replays/" + video_name + '.mp4')

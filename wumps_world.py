import matplotlib.pyplot as plt  
import random  


class WumpusWorld:
    def __init__(self):
        self.grid_size = 4
        self.agent_pos = (0, 0)  
        self.agent_dir = "right"
        self.has_gold = False
        self.has_arrow = True
        self.wumpus_alive = True
        self.world = self.generate_world()
        self.percepts = self.get_percepts()

    def generate_world(self):
        world = [[{"pit": False, "wumpus": False, "gold": False} for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if (i, j) != (0, 0) and random.random() < 0.2:
                    world[i][j]["pit"] = True
        wumpus_pos = (random.randint(0, 3), random.randint(0, 3))
        while wumpus_pos == (0, 0):
            wumpus_pos = (random.randint(0, 3), random.randint(0, 3))
        world[wumpus_pos[0]][wumpus_pos[1]]["wumpus"] = True
        gold_pos = (random.randint(0, 3), random.randint(0, 3))
        while gold_pos == (0, 0):
            gold_pos = (random.randint(0, 3), random.randint(0, 3))
        world[gold_pos[0]][gold_pos[1]]["gold"] = True
        return world

    def get_percepts(self):
        x, y = self.agent_pos
        cell = self.world[x][y]
        percepts = {"stench": False, "breeze": False, "glitter": False, "bump": False, "scream": False}
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size:
                if self.world[nx][ny]["wumpus"] and self.wumpus_alive:
                    percepts["stench"] = True
                if self.world[nx][ny]["pit"]:
                    percepts["breeze"] = True
        if cell["gold"]:
            percepts["glitter"] = True
        return percepts

    def is_game_over(self):
        x, y = self.agent_pos
        cell = self.world[x][y]
        if (cell["pit"] or (cell["wumpus"] and self.wumpus_alive)):
            return "lose"
        if self.has_gold and self.agent_pos == (0, 0):
            return "win"
        return "continue"


class LogicAgent:
    def __init__(self, env):
        self.env = env
        self.safe = set()
        self.visited = set()
        self.frontier = [(0, 0)]
        self.current_pos = (0, 0)

    def get_adjacent(self, pos):
        x, y = pos
        adj = []
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 4 and 0 <= ny < 4:
                adj.append((nx, ny))
        return adj

    def update_knowledge(self, percepts):
        self.visited.add(self.current_pos)
        self.safe.add(self.current_pos)
        adj = self.get_adjacent(self.current_pos)

        if not percepts["breeze"] and not percepts["stench"]:
            for cell in adj:
                if cell not in self.safe:
                    self.safe.add(cell)
                if cell not in self.visited and cell not in self.frontier:
                    self.frontier.append(cell)

    def move(self):
        if not self.frontier:
            print("No more safe moves known.")
            return False
        self.current_pos = self.frontier.pop(0)
        self.env.agent_pos = self.current_pos
        percepts = self.env.get_percepts()
        print(f"Agent moved to {self.current_pos}, Percepts: {percepts}")
        if percepts["glitter"]:
            self.env.grab_gold()
            print("✨ Agent grabbed the gold!")
        self.update_knowledge(percepts)
        return True


def draw_world(world, agent_pos):
    fig, ax = plt.subplots()
    for i in range(4):
        for j in range(4):
            cell = world[i][j]
            text = ''
            if cell["pit"]:
                text += 'P '
            if cell["wumpus"]:
                text += 'W '
            if cell["gold"]:
                text += 'G '
            if (i, j) == agent_pos:
                text += 'A '

            ax.text(j, 3 - i, text.strip(), ha='center', va='center', fontsize=12)
            ax.add_patch(plt.Rectangle((j, 3 - i), 1, 1, fill=False))

    ax.set_xlim(0, 4)
    ax.set_ylim(0, 4)
    ax.set_aspect('equal')
    ax.axis('off')
    plt.title("Wumpus World")
    plt.show()


if __name__ == "__main__":
    env = WumpusWorld()
    agent = LogicAgent(env)

    percepts = env.get_percepts()
    agent.update_knowledge(percepts)
    draw_world(env.world, env.agent_pos)


    for step in range(10):
        print(f"\n--- Step {step + 1} ---")
        success = agent.move()
        draw_world(env.world, env.agent_pos)

        if not success:
            print("❌ No more safe moves. Ending simulation.")
            break

        result = env.is_game_over()
        if result == "win":
            print("🎉 Agent WON the game!")
            break
        elif result == "lose":
            print("💀 Agent LOST the game!")
            break

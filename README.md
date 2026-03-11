🧠 Wumpus World — Logic-Based Intelligent Agent

A Python implementation of the classic Wumpus World environment from AI research, featuring a logic-based intelligent agent that navigates a dangerous grid using knowledge representation and reasoning.

Based on the Wumpus World problem introduced by Gregory Yob (1973) and formalized in Artificial Intelligence: A Modern Approach by Russell & Norvig.

Overview

The Wumpus World is a canonical environment in AI used to illustrate how an intelligent agent can reason under uncertainty using logical inference. The agent must navigate a 4×4 grid, avoid deadly pits and a monster (the Wumpus), and retrieve gold — all without being able to see the full world directly.

This project demonstrates core AI agent design principles through a hands-on simulation with visual output via matplotlib.

Theoretical Concepts

This project serves as a practical showcase of the following AI concepts:

1. 🤖 Intelligent Agents
   
An intelligent agent is anything that perceives its environment through sensors and acts upon it through actuators (Russell & Norvig). This implementation follows the standard agent model:

Component	Implementation

Sensors	get_percepts() — detects stench, breeze, glitter
Actuators	move() — navigates cells in the grid
Agent Function	Maps percept sequences to actions
Agent Program	LogicAgent class

2. 🌍 PEAS Description
   
The agent is defined using the PEAS framework:

Performance Measure — Grab gold, avoid pits & Wumpus, reach exit
Environment — 4×4 partially observable grid
Actuators — Move, grab gold, shoot arrow
Sensors — Stench, breeze, glitter, bump, scream
3. 🔍 Environment Properties
The Wumpus World exhibits several classic environment characteristics:

Property	Value

Observability	Partially observable
Determinism	Deterministic
Episodic vs Sequential	Sequential
Static vs Dynamic	Static
Discrete vs Continuous	Discrete
Single vs Multi-agent	Single agent

4. 🧩 Knowledge Representation
The agent maintains an internal knowledge base representing:

Cells confirmed safe (no pit, no Wumpus)
Cells visited (already explored)
A frontier of candidate safe cells to explore next
This is a simplified form of propositional logic reasoning — the agent infers safety from the absence of percepts (no breeze → no adjacent pit).

5. 🔗 Logical Inference — Modus Ponens
The core reasoning rule applied:

IF current cell has no breeze AND no stench
THEN all adjacent cells are safe
This is an application of Modus Ponens in propositional logic:

P = "No breeze detected at position (x, y)"
P → Q = "No breeze implies no adjacent pits"
∴ Q = "Adjacent cells are safe to visit"

6. 🗺️ Search & Planning
The agent uses a frontier-based exploration strategy:

Maintains a queue of known-safe, unvisited cells
Visits cells in FIFO order (breadth-first style exploration)
Avoids any cell not proven safe (conservative policy under uncertainty)

7. 🎲 Uncertainty & Risk Aversion
Because the environment is partially observable, the agent cannot directly see pits or the Wumpus. It acts risk-aversely only moving to cells logically guaranteed to be safe. This models a key challenge in AI: acting rationally under uncertainty.

Project Structure
wumpus-world/
│
├── wumps_world.py       # Main simulation file
│   ├── WumpusWorld      # Environment class (world generation, percepts, game state)
│   ├── LogicAgent       # Intelligent agent (knowledge base, inference, movement)
│   └── draw_world()     # Matplotlib visualizer
│
└── README.md
How It Works
┌─────────────────────────────────────┐
│           Wumpus World (4×4)        │
│  P = Pit   W = Wumpus   G = Gold   │
│  A = Agent                          │
└─────────────────────────────────────┘
          │
          ▼
  Agent senses percepts
  (stench / breeze / glitter)
          │
          ▼
  Updates knowledge base
  (safe cells, frontier)
          │
          ▼
  Selects next safe cell
  from frontier queue
          │
          ▼
  Moves & checks game state
  (win / lose / continue)
Win condition: Agent grabs the gold and returns to (0,0).
Lose condition: Agent steps into a pit or a living Wumpus's cell.



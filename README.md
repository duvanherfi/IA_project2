# IA_project2

Coursework — Artificial Intelligence, Universidad del Valle (2024).

Depth-limited **minimax** over a game tree with a heuristic utility function,
playable through a pygame interface. The game tree is built up to a depth
limit (`crearArbol`) and walked back up (`recorrerMinimax`) to pick the move,
so the depth limit and the heuristic are what decide how well the machine
plays.

## Running it

```bash
pip install -r requirements.txt
python Interfaz.py
```

Any library you add belongs in `requirements.txt`.

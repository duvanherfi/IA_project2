"""Regenerate the images in the README.

Plays a full game off-screen — the machine picking its move with minimax, a
scripted opponent standing in for the human — and writes the frames to docs/ as
a still and an animated GIF.

    pip install -r requirements.txt pillow
    python tools/record_demo.py
"""
import os
import random
import sys
import time

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(REPO, "docs")

# Render to an off-screen surface so this runs without a window manager.
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.chdir(REPO)
sys.path.insert(0, REPO)

import numpy as np  # noqa: E402
import pygame  # noqa: E402
from PIL import Image  # noqa: E402

from Interfaz import Tablero  # noqa: E402

SEED = 7          # any fixed seed; this one gives a game that reads well
MAX_TURNS = 120   # the game always ends well before this

PLAYER_TRAIL = 4  # cells the human side has claimed
MACHINE_TRAIL = 5


def new_game(level):
    """A board that is the same on every run, so the README cannot drift."""
    random.seed(SEED)
    seed = random.seed
    random.seed = lambda *args, **kwargs: None  # iniciar_nivel reseeds on the clock
    try:
        board = Tablero()
        board.nivel = level
        board.iniciar_nivel()
    finally:
        random.seed = seed
    board.menu = False
    return board


def frame(board):
    """Draw one frame the way Tablero.main_loop would, minus the mouse preview."""
    pending, board.jugadas_2 = board.jugadas_2, []
    board.pantalla.fill(board.NEGRO)
    board.draw_loop()
    board.draw_resumen()
    if board.fin:
        board.draw_ganador()
    pygame.display.flip()
    board.jugadas_2 = pending

    surface = pygame.display.get_surface()
    return Image.frombytes("RGB", surface.get_size(), pygame.image.tostring(surface, "RGB"))


def human_move(board):
    """Stand-in for the person: take the move that claims the most cells.

    Deliberately shallow — it looks one move ahead and never at what the machine
    can answer. The point of the recording is the machine's search, not this.
    """
    options = board.jugadas_2[1:]  # entry 0 is the position as it stands
    if not options:
        return None
    return max(options, key=lambda grid: np.count_nonzero(np.array(grid) == PLAYER_TRAIL))


def play(level):
    board = new_game(level)
    frames = [frame(board)]
    turns = 0

    for _ in range(MAX_TURNS):
        if board.fin:
            break

        board.time_init = 0  # skip the pause the interface puts between turns
        board.turno_maq()
        turns += 1
        frames.append(frame(board))
        if board.fin:
            break

        board.calcular_mov_jug()
        chosen = human_move(board)
        if chosen is not None:
            board.grid = chosen
            board.grid_inicial = chosen
            board.turno = 1
        # Leave jugadas_2 alone: turno_maq reads it to decide the game is over,
        # which happens when neither knight has a square left to jump to.
        frames.append(frame(board))

    frames.append(frame(board))
    result = {
        "machine": board.jugadasm(),
        "player": board.jugadasj(),
        "winner": board.ganador(),
        "depth": board.profundidad,
        "turns": turns,
    }
    pygame.quit()
    return frames, result


def save_gif(frames, path, scale=0.75, ms=420, hold=8):
    width, height = frames[0].size
    size = (int(width * scale), int(height * scale))
    resized = [f.resize(size, Image.LANCZOS).quantize(colors=32, method=Image.MEDIANCUT)
               for f in frames]
    resized = resized + [resized[-1]] * hold
    resized[0].save(path, save_all=True, append_images=resized[1:],
                    duration=ms, loop=0, optimize=True, disposal=2)


if __name__ == "__main__":
    os.makedirs(DOCS, exist_ok=True)
    for level, name in [(0, "beginner"), (1, "amateur"), (2, "expert")]:
        started = time.time()
        frames, result = play(level)
        elapsed = time.time() - started
        save_gif(frames, os.path.join(DOCS, f"{name}.gif"))
        if name == "expert":
            frames[0].save(os.path.join(DOCS, "board.png"))
        size = os.path.getsize(os.path.join(DOCS, f"{name}.gif")) // 1024
        print(f"{name:9s} depth {result['depth']}  {result['turns']:3d} turns  "
              f"machine {result['machine']:3d} - player {result['player']:3d}  "
              f"winner {result['winner']:8s}  {elapsed:6.2f}s of search  "
              f"docs/{name}.gif ({size} KB)")

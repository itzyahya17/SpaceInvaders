# Space Invader
### AoICT Lab Project — BCS 1-B
**Made by: Muhammad Yahya**

---

## About the Game

Space Invader is a 2D space shooter game built with Python and Pygame. You control an orange spaceship at the bottom of the screen and must destroy waves of alien enemies across 5 levels. Each level gets faster, harder, and throws more enemies at you. Destroy all enemies on each level to advance. If your health reaches zero, it is game over.

---

## Project Structure

```
Space Invaders (Game)/
├── main.py          — Game loop, all screens, input handling
├── ships.py         — Player, Enemy, Laser classes
├── levels.py        — Enemy formations for each level
├── settings.py      — Window setup, image loading
├── highscore.txt    — Saves your best score automatically
├── assets/          — All image files (ships, lasers, background)
└── sounds/          — All sound effects
```

---

## Requirements

- Python 3.10, 3.11, or 3.12
- Pygame 2.x

Note: Python 3.13 and 3.14 are NOT supported by Pygame yet.

---

## Installation

Step 1 — Install Python 3.12

Download from: https://www.python.org/downloads/release/python-31210/
Download the Windows installer (64-bit) and run it.
Check "Add Python to PATH" during installation.

Step 2 — Install Pygame

Open CMD or PowerShell and run:

    py -3.12 -m pip install pygame --prefer-binary

Step 3 — Run the game

Navigate to the game folder in CMD:

    cd "C:\Users\YourName\Desktop\Space Invaders (Game)"

Then run:

    py -3.12 main.py

---

## Controls

| Key         | Action                      |
|-------------|-----------------------------|
| Left Arrow  | Move left                   |
| Right Arrow | Move right                  |
| Up Arrow    | Move up                     |
| Down Arrow  | Move down                   |
| Space       | Shoot                       |
| ESC         | Pause / Unpause             |
| Enter       | Confirm / Start             |
| M           | Main Menu                   |
| R           | Reset High Score (on menu)  |

---

## Levels

| Level | Enemies | Formation       | Difficulty            |
|-------|---------|-----------------|-----------------------|
| 1     | 6       | Single row      | Slow, light shooting  |
| 2     | 9       | Two rows        | Medium speed          |
| 3     | 7       | V formation     | All 3 enemy types     |
| 4     | 9       | Three columns   | Fast, heavy shooting  |
| 5     | 14      | Row + V shape   | Fastest, hardest      |

---

## Enemy Types

Enemies change appearance as their health drops:

| Color | Health | Hits to Kill | Points |
|-------|--------|--------------|--------|
| Green | 30 hp  | 3 hits       | 30 pts |
| Red   | 20 hp  | 2 hits       | 20 pts |
| Blue  | 10 hp  | 1 hit        | 10 pts |

An enemy that starts green will turn red then blue as you shoot it.

---

## Player Health Per Level

| Level | Player Health |
|-------|---------------|
| 1     | 100           |
| 2     | 120           |
| 3     | 150           |
| 4     | 180           |
| 5     | 220           |

---

## File Descriptions

main.py
The main file. Contains the game loop which runs 90 times per second. Handles all screens (menu, game over, you won, pause, level intro), player input, enemy logic, collision detection, score tracking, and sound playback.

ships.py
Contains 4 things — the collide function for pixel-perfect collision detection, the Laser class for bullets, the Ship base class with shared logic, and the Player and Enemy classes which both inherit from Ship.

levels.py
Defines the enemy formation for each of the 5 levels. Uses a helper function make_enemy() to create enemies with specific health, speed, position, and shoot frequency. Stores all spawner functions in a dictionary called LEVEL_SPAWNERS so main.py can call the right one automatically.

settings.py
Runs first. Creates the game window and loads all image files into variables. Every other file imports from here so images are only loaded once.

---

## High Score

The high score is saved automatically to highscore.txt in the game folder. It stays saved even after closing the game. Press R on the main menu to reset it to 0.

---

## Common Errors

ModuleNotFoundError: No module named pygame
Pygame is not installed for the Python version you are using. Run:
    py -3.12 -m pip install pygame --prefer-binary

Failed to build pygame when getting requirements
Your Python version is too new. Install Python 3.12 specifically.

Game window does not open
Make sure you are running the file from inside the game folder, not a parent folder.

Daksh Upadhyay - 100008300
 
 Neon Relic

 Game Concept
Neon Relic is a single-player 2D top-down survival shooter built with Pygame. You control a
glowing orb in a neon arena, fighting off waves of enemies that spawn from the screen edges
and home in on you. Enemies get faster and tougher as your score climbs, so the pressure
ramps up the longer you survive.

To stay alive you can dash out of danger, land a powerful area-of-effect "wave" ultimate once
it's charged, and grab pickups scattered around the map: crystals restore health and add
score, while a portal occasionally appears and grants a temporary rapid-fire buff. The goal is
simple — rack up as high a score as possible before you run out of health.

 Controls
- WASD — move
- Mouse (left click)** — shoot toward cursor
- SPACE — dash
- E — charge and release the wave ultimate
- P — pause / resume
- Q (while paused) — toggle auto-shoot (auto-fires at the nearest enemy)
- ESC (on game over screen) — restart

 How to Run
1. Make sure Python 3 is installed.
2. Install the one dependency:
   ```
   pip install pygame
   ```
3. Run the game:
   ```
   python game.py
   ```

 Classes Implemented (5 required, 5 provided)
- Player — handles movement, dashing, shooting, the ultimate charge/detonate cycle, and
  drawing the player with its buff/charge indicator rings.
- Enemy — spawns at random screen edges, scales in speed/health with difficulty, and
  chases the player each frame.
- Bullet — represents both normal and "powered" projectiles (fired from the ultimate or
  while portal-buffed), with different speed/damage/visuals depending on type.
- Crystal — a rotating pickup that heals the player and adds score on contact, spawning
  periodically over time.
- Portal — a temporary pickup that appears once a score threshold is hit, granting the
  player a rapid-fire buff if reached before it expires.

 Additional Features Beyond the Base Tutorial
- Dash mechanic with its own cooldown
- Chargeable ultimate ("wave") that fires a ring of bullets and damages all nearby enemies
- Difficulty scaling over time (enemy spawn rate, enemy speed, and enemy health all increase)
- Portal power-up system with its own countdown/expiry
- Toggleable auto-shoot mode that targets the nearest enemy
- Full pause menu and game-over/restart flow with a live HUD (health bar, dash/ult cooldown
  status, score, current difficulty speed multiplier)

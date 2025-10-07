
## 🛸 Space Invaders - Advanced (Python + Pygame)

A modern, feature-rich version of the classic **Space Invaders** arcade game built using **Python** and **Pygame**.  
Includes power-ups, boss battles, particle effects, shields, and level progression.

---

### 🚀 Features

- 👾 Dynamic Enemy Waves  
- 🧠 Boss Battles every 5 levels  
- ⚡ Power-ups (Rapid Fire, Spread Shot, Shield, Bonus Score)  
- 💥 Particle Explosions  
- 🧱 Destructible Shields  
- 💾 Persistent High Score  
- 🎵 Sound Effects & Music (optional)  
- 🕹️ Pause, Restart, and Mute options  
- 🎮 Smooth OOP-based gameplay system  

---

### 🧩 Requirements

Make sure you have:
- **Python 3.8+**
- **Pygame library**

Install Pygame using pip:
```bash
pip install pygame
```

---

### 📂 Project Structure

```
space-invaders/
│
├── space_invaders_advanced.py   # Main game file
├── RUN.md                       # This file
├── assets/                      # (Optional) Images & sounds
│   ├── player.png
│   ├── enemy.png
│   ├── boss.png
│   ├── shoot.wav
│   ├── explode.wav
│   ├── powerup.wav
│   └── hit.wav
└── si_highscore.json            # Created automatically to store high scores
```

> 🖼️ The game works even without the `assets/` folder — it will use fallback graphics and silent mode.

---

### ▶️ How to Run

1. Open a terminal or command prompt in the project folder.  
2. Run the game using:
   ```bash
   python space_invaders_advanced.py
   ```
3. Enjoy playing! 🎮  

---

### 🎮 Controls

| Key | Action |
|-----|---------|
| ← / A | Move Left |
| → / D | Move Right |
| SPACE | Shoot |
| P | Pause / Resume |
| M | Mute / Unmute |
| R | Restart (after Game Over) |
| ESC | Quit |

---

### 🧠 Gameplay Tips

- **Collect Power-ups:** Yellow circles drop randomly — grab them for powerful temporary abilities.  
- **Stay Mobile:** Enemies and the boss fire bullets; movement is key!  
- **Shields:** Hide behind shields, but note — they degrade when hit.  
- **Boss Levels:** Every 5 levels you face a boss with stronger attacks.  

---

### 🏆 Scoring System

| Action | Points |
|--------|---------|
| Destroy Enemy | 10–25 |
| Collect Power-up | +200 |
| Defeat Boss | +500 |

Your **high score** is saved automatically between game sessions.

---

### 🧰 Troubleshooting

- **Pygame not found?**  
  → Run `pip install pygame`
  
- **Game window not appearing?**  
  → Make sure Python 3 is installed correctly.

- **No sound?**  
  → Add `.wav` files inside `assets/` or check that your audio device works.

---

### 📦 Build Executable (Optional)

If you want to make a `.exe` (Windows standalone):

```bash
pip install pyinstaller
pyinstaller --onefile --noconsole space_invaders_advanced.py
```

This will create an executable in the `dist/` folder.

---

### 💡 Future Enhancements

- Gamepad support  
- Leaderboard system  
- Background music  
- Web (browser) version using Pyodide or Phaser  

---

 

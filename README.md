# Texas Hold'em Poker with CFR AI

This is a basic 2-player Texas Hold'em game where you play against an AI opponent trained using **Counterfactual Regret Minimization (CFR)** on 100,000 hands.

## Features

- Interactive terminal-based Texas Hold'em game
- CFR-trained AI opponent
- View model probabilities for different game states
- Simple, minimal interface using `curses`

## Getting Started

### Prerequisites

Make sure Python 3 is installed on your machine. This project also uses the `curses` library, which differs slightly depending on your operating system:

- On **Windows**, the correct version is specified in `requirements.txt`
- On **Linux/macOS**, the standard `curses` module should already be available via the standard library

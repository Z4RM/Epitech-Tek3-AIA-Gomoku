# ⚠️ This repository is dedicated to (the research of) [@Clement-Z4RM](https://github.com/Clement-Z4RM), last seen on GitHub on Thursday, November 14, 2024 morning. If you have any information, please contact us. Your help is greatly appreciated.

# Gomoku AI Bot

### Table of Contents
- [Overview](#overview)
- [Game Rules](#game-rules)
- [Features](#features)
- [Technical Details](#technical-details)
- [Getting Started](#getting-started)
- [Contact](#contact)
- [Authors](#authors)

## Overview

Welcome to the **Gomoku AI Bot** repository.
This project focuses on building a bot for the *Gomoku Narabe* (also called *Wuzi Qi*, *Slope*, *Darpion* or *Five in a Row*) board game using artificial intelligence techniques.
*Gomoku* is a two-player strategy game where the objective is to be the first to get five stones in a row on a 20x20 grid.

The **Gomoku AI Bot** is an artificial intelligence developed to play to the *Gomoku* game. Its goal is to play *Gomoku* against another AI or a human in order to win the game.

## Game Rules

- Played on a 20x20 game board, also called a *goban* (game board size is decided by the server, but 20x20 is the generally used size).
- Two players alternate turns placing stones.
- The first player to align **five stones in a row** (horizontally, vertically, or diagonally) wins.

## Features

- Implements smart algorithms for optimal performance.
- Handles edge cases and winning strategies.
- Adheres to the *Epitech Gomoku* communication protocol for seamless integration with other bots.
- Compatible with *Gomoku* interfaces like Piskvork or Liskvork.

## Technical Details

### Software Requirements
- **Python:** Version 3.12 or higher.

#### Installation:
1. Ensure Python is installed:
   ```bash
   python3 --version
   ```
   If not installed, install Python 3:
   ```bash
   sudo apt-get update
   sudo apt-get install python3
   ```
   The above command is for Debian-based systems (Debian, Ubuntu...). 
   If you are on another system, you can download it directly from the [Python website](https://www.python.org/downloads), or search for the installation steps for your system on internet.

### Communication Protocol:
The bot follows the *Epitech Gomoku* protocol for interaction with the server: [PROTOCOL.md](PROTOCOL.md).

## Getting Started

### Installation:
1. Clone the repository:
   ```bash
   git clone https://github.com/Z4RM/Epitech-Tek3-AIA-Gomoku
   cd gomoku-ai
   ```

### Configuration

The configuration file must be named `bot.ini` and located at the same path as the one where the server (or bot when testing/debugging) is launched.
All the keys from the configuration file have default values, so this file is not mandatory and the bot will work properly even if it is not present.

First of all, copy the `bot.ini.example` file and rename it to `bot.ini`. You can then set your own configuration keys in this new file.

Here is a list of the keys and their description (also summarized directly in the config file):
- `bot` - Information about the bot. They are mainly basic information without big impact on the comportement of the program/bot.\
  When the server sends the command `ABOUT` to the bot, it sends back this information in this format: `name="<name>", version="<verion>", author="<author>", country="<country>"`
  - `name` - The name of the bot. Used, among others, in the logs.
  - `version` - The version of the bot.
  - `author` - The author of the bot.
  - `country` - The country of the bot.
- `log` - The bot can log information in a file for debugging or simply get information on its status, etc.
  - `level` - The log level, from `None` (default) to `Debug`.
    - In `None` mode, no log is writen. The file is not even opened/created.
    - In `Fatal` mode, only fatal errors (errors that prevent execution from continuing) are writen.
    - In `Error` mode, all errors (e.g. when the bot send back to the server `ERROR [error message]`) and logs of a higher level (`Fatal`) are writen.
    - In `Warn` mode, all warnings and logs of a higher level (`Fatal` and `Error`) are writen.
    - In `Info` mode, all information logs (e.g. the bot is running or stopped) and logs of a higher level (`Fatal`, `Error` and `Debug`) are writen.
    - In `Debug` mode, all logs are writen: command received, executed, etc and logs of a higher level (`Fatal`, `Error`, `Debug` and `Info`) are writen.
  - `file` - The file where to write the logs to. Can be a relative (from where the server/bot is launched) or an absolute path.

### Run the Bot:
- Start the bot by executing:
  ```bash
  ./pbrain-gomoku-ai
  ```
- You can test the bot against other AI using programs like [Liskvork](https://github.com/Epitech/B-AIA-500_liskvork) or other Gomoku "server" interfaces.

## Contact

For inquiries or contributions, please open an issue or submit a pull request on the GitHub repository.

## Authors

- ~~[@Clement-Z4RM](https://github.com/Clement-Z4RM)~~ (missing since Thursday, November 14, 2024)
- [@josephinecr](https://github.com/josephinecr)
- [@MathisZucchero](https://github.com/MathisZucchero)
- [@Z4RM](https://github.com/Z4RM)

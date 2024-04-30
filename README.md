# toohak

Toohak is a distributed online competition game inspired by Kahoot. The game
enables multiple players to participate simultaneously, answering the same set
of questions at their own pace and viewing a leaderboard that displays the top
five players' progress.

## Installation

To run the game, make sure that your Python version is **3.12** or above. From
source directory, run `make install` to install all the necessary dependencies.

## Playing

1. `source .venv/bin/activate`
2. In one terminal, run `make server` and copy the server IP address from the terminal.
3. In another terminal, run `make client` and paste the server IP address to begin.

## Directory Structure

```
toohak
├── Makefile
├── README.md
├── assets
├── requirements.txt
└── src
    ├── client.py
    ├── server.py
    ├── modules
    │   ├── __init__.py
    │   ├── __pycache__
    │   ├── network
    │   ├── question
    │   ├── scene
    │   ├── serializable
    │   ├── solution
    │   ├── state
    │   ├── type
    │   └── validator
    └── static
        └── font
```

Let’s go through each directory / file by their functionality:

- Makefile: For compiling and running the program.
- requirements.txt: Lists all the Python package dependencies necessary for the project, ensuring consistent setups across different environments.
- README.md: Provides an overview of the project and instructions to run the code.
- assets: A directory that contains media file for this program like the background music.
- src: Main application codes.
  - client.py: The entrance point and main logics for a client process.
  - server.py: The entrance point and main logics for a server process.
  - modules: Encapsulates specific functionalities by definitions of different classes or modules that support different aspects of the game.
  - network: Message protocols for the clients to communicate with the server.
  - question: Defines question types and builders such as MultipleChoiceQuestionBuilder.
  - scene: All the frontend pygame scenes are stored here, which are all inherited from the AbstractScene as introduced in our architecture overview.
  - serializable: Protocols for encoding (serializing) and decoding messages.
  - solution: Defines solution types and builders.
  - state: Defines and exports ServerState and PlayerState to be used by server.py and client.py.
  - type: Defines global type aliases for code clarity since we use type annotation heavily.
  - validator: Validates IP address.

## Precautions

> ❌ Do not quit the game mid-way. This would result in an unpredictable state, where the client would deadlock on the final scene.

> ⚠️ The server needs to be restarted after completing 1 round.

> ⚠️ Players can't join mid-game.

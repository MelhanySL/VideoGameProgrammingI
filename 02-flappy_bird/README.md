# Flappy Bird: Hard Mode & Mechanics Update

Implementation of advanced game features including a Pause State, a new Hard Mode, and a Ghost Power-Up.

## Context

This update expands upon the base Flappy Bird game by introducing the Strategy Pattern for different game modes, the Factory Pattern for spawning entities, and an interruptible Pause State that preserves the game environment.

## Controls

* **`Up Arrow`**: Makes the bird jump.
* **`Left Arrow`**: Moves the bird left (Hard Mode only).
* **`Right Arrow`**: Moves the bird right (Hard Mode only).
* **`Space`**: Toggles the Pause State (freezes/resumes the game).
* **`Enter`**: Confirms state transitions (starts game, selects mode).
* **`Escape`**: Exits the application.

## Architecture & Changes

* **Pause State**: 
  * Added `PauseState` which retains references to `World`, `Bird`, `mode`, and `score`.
  * Halts all `dt` updates and pauses background music. Reverting to `PlayingState` resumes execution seamlessly.
* **Game Modes (Strategy Pattern)**: 
  * Abstracted game rules into `FlappyGameMode` with `NormalMode` and `HardMode` implementations.
  * `NormalMode` retains standard Flappy Bird physics and log generation.
* **Hard Mode Mechanics**:
  * Enables horizontal movement (`vx`) for the bird.
  * Log pairs are generated dynamically using `LogProfile` weights, resulting in variable gaps, spawn intervals, and vertical shifts.
  * Introduces moving logs that close and open their vertical gaps, triggering a collision sound upon fully closing.
* **Ghost Power-Up (Factory Pattern)**:
  * Spawns periodically in Hard Mode.
  * When consumed, grants temporary invulnerability (`GHOSTING_TIME`), allowing the bird to pass through logs.
  * Replaces standard background music with a booster track and applies a ghost texture to the bird while active.
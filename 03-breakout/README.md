# Breakout: Power-Ups & Mechanics Update

Implementation of advanced game features including a dynamic Pause State, various Power-Ups using the Abstract Factory pattern, and shooting mechanics.

## Context

This update expands upon the base Breakout game by introducing multiple power-ups, complex entity interactions (like bullets and shields), and an interruptible Pause State that fully preserves the game's state (including active projectiles and power-ups).

## Controls

* **`Left Arrow`**: Moves the paddle to the left.
* **`Right Arrow`**: Moves the paddle to the right.
* **`Space`**: Shoots bullets (when the Cannon power-up is active).
* **`Pause Key`** *(Space)*: Releases caught balls (if the Ball Catch power-up is active). If no balls are currently caught, it toggles the Pause State (freezes/resumes the game).
* **`Escape`**: Exits the application.

## Architecture & Changes

* **Power-Ups (Abstract Factory Pattern)**:
  * Modular implementation of temporary enhancements spawned from destroyed bricks.
  * **CannonPower**: Equips the paddle with cannons to shoot bullets (`Space`) that destroy bricks.
  * **ShieldPower**: Generates a protective barrier at the bottom of the screen that bounces the ball back into play.
  * **BallCatch**: Allows the paddle to catch and hold the ball upon impact. The ball can be released using the pause/action key.
  * **TwoMoreBall**: Spawns two additional balls, creating a multiball scenario.
* **Pause State**:
  * Passes all active environment variables (bullets, power-ups, active shields, multiple balls) via `params` to ensure no data is lost or desynced when resuming the game.
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

### ShieldPower (Protective Barrier)

* **Overview**: 
  The `ShieldPower` is a single-use defensive enhancement designed to prevent ball loss. When collected by the paddle, it deploys a temporary, single-use protective barrier across the full virtual width of the screen, situated directly above the bottom boundary.

* **Technical Execution & Rendering**:
  * **Collision Detection & Physics**: During the `PlayState` update cycle, if `shield_active` is evaluated as `True`, the ball's Y-coordinate is intercepted before reaching the outer world bounds. 
  * **Impulse Reversal**: Upon contact with the shield, the vertical velocity component (`vy`) is forcefully inverted using `-abs(ball.vy)`, reflecting the ball upward regardless of its downward momentum angle.
  * **State Persistence**: The active state of the shield (`shield_active`) is explicitly serialized through the `params` dictionary during `PauseState` transitions, guaranteeing that active barriers remain persistent when resuming the session.
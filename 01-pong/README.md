# Pong AI Implementation

AI-controlled left paddle (Player 1) implementation inside `PlayState`.

## Context

The module replaces manual human input for Player 1 with an automated tracking script while maintaining standard physics and speed limits.

## Controls

* **`Up Arrow`**: Moves Player 2 paddle upward.
* **`Down Arrow`**: Moves Player 2 paddle downward.
* **`Enter`**: Confirms state transitions (starts game from title, serves ball, restarts after match).
* **`Escape`**: Exits the application.
* **`W` / `S`**: Disabled (Player 1 is automated by AI).

## AI Mechanics

* Evaluates the Y-axis position of the ball relative to the paddle center only when `ball.x < VIRTUAL_WIDTH / 2`.
* Applies a $\pm 2\text{ px}$ threshold around `ball_center`. If `paddle_center` is within this range, `vy` is set to `0` to prevent oscillation.
* Assigns `vy = PADDLE_SPEED` or `vy = -PADDLE_SPEED` depending on whether `paddle_center` is above or below the target threshold.

## Input Configuration

* Player 1 input bindings (`p1_up`, `p1_down`) are removed from `PlayState.on_input()`.
* Player 2 retains manual keyboard control via `p2_up` and `p2_down`.
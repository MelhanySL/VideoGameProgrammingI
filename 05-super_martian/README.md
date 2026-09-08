# Super Martian: Level Progression & Mechanics Update

Implementation of new level designs, score-based interactable blocks, and state transition effects for the Super Martian platformer.

## Context

This update expands upon the base Super Martian game by introducing a new Tiled-based level (Level 2), interactive target-score blocks, animated item spawning, and an interruptible level transition system that freezes game state while rendering a cartoon-style iris effect.

## Controls

* **`Left Arrow` / `A`**: Moves the player left.
* **`Right Arrow` / `D`**: Moves the player right.
* **`Up Arrow` / `W`**: Climbs up ladders.
* **`Down Arrow` / `S`**: Climbs down ladders.
* **`Space` / `Left Click`**: Makes the player jump.
* **`P`**: Toggles the Pause State (freezes/resumes the game).
* **`Enter`**: Confirms state transitions.
* **`Escape`**: Exits the application.

## Changes

* Added `level2.json` built with Tiled, featuring new structural layouts, ladder placements, creatures, and coin distributions.
* Introduced a specialized solid block that tracks the player's score. The block materializes only when the player reaches a defined `target_score` (for example: 190 in Level 1 and 500 in Level 2).
* Hitting the block from below dynamically spawns a Key item.
* The Key uses a tweening animation to simulate popping out of the block, with collisions temporarily disabled during the upward movement to ensure smooth visual delivery.
* Collecting the Key serves as the immediate level completion trigger.
* Halts the timer, disables player input, and freezes entity updates to preserve the exact game state.
* Renders a cartoon-style "iris" (closing circle) visual transition before swapping to the next level or the Victory State.
* Plays a dedicated audio cue to provide clear sonic feedback of completion.
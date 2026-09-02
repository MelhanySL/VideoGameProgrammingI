# Match-3: Mechanics & Power-Ups Update

Implementation of Match-3 game features, including a Drag & Drop interaction system, strict move validation, automatic reshuffling, and Power-Ups.

## Controls

* **`Left Mouse Click (Hold)`**: Grabs and attaches a tile to the mouse cursor for dragging.
* **`Left Mouse Release`**: Drops the tile to attempt a swap with the underlying adjacent tile.
* **`Left Mouse Click (Press)`**: Instantly detonates a clicked Power-Up tile, if one is present.
* **`Enter`**: Confirms state transitions and menu selections.
* **`Escape`**: Exits the application.

## Architecture & Changes

* Transitioned from a click-to-select logic to a continuous drag-and-drop system.
* The game strictly restricts moves that do not result in a match.
* Integrated a deadlock resolution loop to ensure continuous gameplay.
* If the board stabilizes and `matches_possible()` returns `False`, a `while` loop triggers `_initialize_tiles()` recursively until the matrix guarantees at least one valid swap for the player.

* **Power-Ups**:
  * Implemented `LineClear` and `ColorBomb` classes inheriting from the base `Tile` class.
  * **Line Clear**: Spawns upon matching 4 tiles. Activation destroys all tiles within the intersecting row and column.
  * **Color Bomb**: Spawns upon matching 5 or more tiles. Activation wipes out all tiles sharing its color across the entire board.

  * Power-ups detonate either by direct clicking or organically by dragging them into a standard color combination.
  * The presence of a power-up prevents the board from automatically reshuffling, as the player can still make a valid move by detonating it.
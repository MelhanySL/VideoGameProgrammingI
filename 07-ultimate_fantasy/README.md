# Ultimate Fantasy: Out-of-Combat Menus & Cooldown-Based Turn System

Implementation of RPG mechanics including a detailed Pause Menu and a Cooldown-Based Turn System.

## Context

This update expands upon the base Ultimate Fantasy game by introducing UI state management for out-of-combat character actions, and revamps the classic turn-based battle system into a dynamic cooldown-driven experience.

## Controls

* **`Up/Down/Left/Right Arrows`**: Move the character in the overworld / Navigate menus.
* **`Enter / Space`**: Confirm selection / Interact / Advance dialogue.
* **`P Key`**: Open the Pause Menu in the overworld.
* **`Escape`**: Quit the game instantly.

## Architecture & Changes

* **Character Status Panel**: 
  * Designed a new GUI inside the `PauseMenuState` that displays the information of each party member inside their own persistent panel.
  * Shows Level, HP (with a visual progress bar), MP, and EXP (with a visual progress bar).
  * If a character is dead, their HP is clamped to 0, the progress bar is emptied, and a red "DEATH" text is displayed.
* **Out-of-Combat Actions (Pause Menu)**: 
  * Added an Actions sub-menu to display the abilities of each player.
  * Attack actions are disabled and rendered with a semi-transparent dark overlay (`alpha` value).
  * Healing actions remain selectable.
* **Overworld Healing Execution**:
  * **Individual Healing**: Selecting a single-target heal allows the player to choose the target (using a specialized `PauseSelectTargetState`), replicating the exact UI flow used in battles.
  * **Global Healing**: Area-of-Effect healing executes exactly as it does in the battle state, restoring HP to all party members simultaneously.
* **Active Time Battle (Cooldown) System**:
  * **Rest Mechanics**: Each battle entity now has an assigned rest time (`cooldown`) defined in `entity.py` that varies depending on the action performed (for example, strong magic requires more rest than a basic attack).
  * **Turn Management**: In the `TakeTurnState`'s `update` method, each entity's cooldown timer decreases over time. The first entity to complete its rest time (cooldown reaches `<= 0`) immediately obtains the turn to act.
  * **Visual Cooldown Indicators**: Added floating dynamic countdown timers in the `BattleState` that display the remaining rest time (in seconds) directly above each character and enemy. The text color turns green and displays "READY!" when it's their turn to act.
  * **Action Menu Enhancements**: The action selection menu in combat proactively displays the time cost next to each ability (for example, `Flame (4.5s)`), allowing players to make strategic decisions based on speed.
  * **Fast-Skipping**: The `Nothing` action has been optimized with a drastically reduced 1.0-second cooldown, providing players with a viable tactical option to briefly delay a character's turn without heavily penalizing them.

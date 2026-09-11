# The Legend of the Princess: Combat Mechanics & Boss Encounter Update

Implementation of ranged combat interactions, conditional room transitions, random Chest spawn system, and a multi-phase boss fight.

## Controls

* **`Up / Down / Left / Right Arrows`**: Moves the player character (Updates the player's spatial coordinates and facing direction).
* **`Space`**: Swings the sword.
* **`F Key`**: Shoots an arrow (only available after acquiring the Bow).
* **`Enter`**: Action (Interact) / Confirm.
* **`Escape`**: Exits the application.

## Architecture & Changes
* **Chest and Bow System**:
  * A chest spawns randomly in a room. It is guaranteed to generate eventually but will only spawn exactly once per playthrough. The dungeon generator tracks a player state flag to ensure a chest spawns randomly on the grid.
  * The player can open the chest by standing directly in front of it and interacting. Opening the chest grants the Bow.
  * Upon acquiring the bow, the player can shoot arrows. Firing the bow executes a dedicated method that reads the player's current coordinates and facing direction to instantiate an arrow `Projectile`, pushing it into the room's active update loop.

* **Vampire Boss Room**:
  * Once the bow is obtained, crossing a doorway introduces a probability of transitioning into the Boss Room, stripping away all minor creatures, interactable pots, and switches.
  * The room is forced to load a single entrance door while spawning the Vampire Boss entity on the exact opposite side of the arena.
  * The boss targets the player by spawning slow-moving fireball projectiles aimed at the player's exact location at the moment of firing.
  * The boss features its own hitpoint pool and is completely immune to sword strikes by default. Hitting the boss with an arrow temporarily shatters this immunity for a few seconds, opening a short window where sword damage is registered.
  * Direct body contact with the boss drains one full heart (2 HP). If a fireball projectile hits the player, it triggers instant death.
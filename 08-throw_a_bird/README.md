# Throw a Bird: Multi-Bird Split Mechanic

Implementation of a mid-air split mechanic for the bird projectile, featuring collision-based ability locking and turn idle detection.

## Context

This update expands upon the base physics trajectory game (Throw a Bird) by introducing a mid-air split ability. It incorporates vector manipulation for velocity deflection, modifies the bird entity to track collision states to restrict ability usage, and updates the physics simulation loop to handle multiple active projectiles simultaneously before resolving the turn.

## Controls

* **`Mouse Left Click & Drag`**: 
  * Near the bird: Pulls the bird back on the slingshot to aim.
  * Elsewhere: Pans the camera across the level.
* **`Mouse Release`**: Flings the bird applying a physics impulse proportional to the drag distance.
* **`Space`**: Triggers the split ability mid-flight (divides the bird into three).
* **`Escape`**: Exits the application.

## Architecture & Changes

* **Split Mechanic (`Bird.py` & `PlayState.py`)**:
  * Added a `clone_with_deviation` method to the `Bird` entity, which safely spawns a clone using Pygame's `Vector2.rotate` to deflect its velocity angle.
  * When pressing `Space` during flight, the main bird clones itself twice. The main bird maintains its original trajectory, while the two new clones branch off at +15 and -15 degree angles with the same initial speed.
* **Collision Restriction (`Bird.py`)**:
  * Added a `check_collisions` method to track physics contacts (`touching_bodies`), actively ignoring background sensors like wind zones.
  * The split ability is strictly disabled the moment the bird registers its first impact with the ground or a tower block, preventing post-crash splitting.
* **Advanced Idle Detection (`PlayState.py`)**:
  * Refactored the `_update_idle` logic to evaluate the physical state of all active clones, rather than just the main bird.
  * The turn is kept alive as long as any bird (the original or any of its clones) maintains significant linear or angular velocity, preventing premature camera resets while sub-birds are still dealing damage.
  * Ensures all clones are properly destroyed and cleared from the Box2D physics world upon turn completion.


## 🤖 AI Implementation

An AI controller was implemented for **Player 1** (the left paddle) inside the `PlayState` class, designed to provide reactive behavior and fair gameplay against a human opponent.

### 📐 Behavior Logic and Strategy

The AI operates using a real-time vertical tracking strategy based on the ball's position, adhering to the following rules:

1. **Limited Reaction Window**: The paddle only begins tracking the ball once it crosses into its half of the table. This introduces a realistic reaction delay, ensuring that high-speed shots can beat the AI if it fails to position itself in time.
2. **Deadzone Handling**: A threshold of $\pm 2$ pixels is set between the center of the ball and the center of the paddle. This prevents high-frequency oscillation when the paddle aligns with the ball.
3. **Fair Play Rules**: The AI's movement speed is strictly restricted to `settings.PADDLE_SPEED`, ensuring it moves at the exact same speed limit as a human player.

### ⚙️ Input Control Adjustments

To enforce single-player control over Player 1:
* The key bindings `p1_up` and `p1_down` were removed from `PlayState`'s `on_input()` method.
* Keyboard inputs are strictly reserved for Player 2.
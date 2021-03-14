import numpy as np

from mesa import Agent


class BLUForce(Agent):
    """
    A BLUForce attack agent.
    The agent follows the following behavior:
        - Locate: Using Satellite-provided data, the agent targets its threat.
        - Navigate: The agent moves in the direction of the target until it is within vision range.
        - Deploy: The agent attacks the target.
    BLUForce agents have a vision that defines the radius in which they look for
    their targets. Their speed (a scalar) and velocity (a vector)
    define their movement.
    """
    
    def __init__(
        self,
        unique_id,
        model,
        pos,
        speed,
        velocity,
        vision,
        enemy, # TODO: Prioritized enemy target list (for now enemy agent)
    ):
        """
        Create a new BLUForce agent.
        Args:
            unique_id: Unique agent identifyer.
            operability: If the asset is operable
            pos: Starting position
            speed: Distance to move per step.
            heading: numpy vector for the agent's direction of movement.
            vision: Radius to look around for enemy threats.
        """
        super().__init__("blu_" + str(unique_id), model)
        self.operability = True
        self.pos = np.array(pos)
        self.speed = speed
        self.velocity = velocity
        self.vision = vision
        self.enemy = enemy
        
    def target_enemy(self):
        """
        Return the vector toward the enemy agent.
        """
        direction = np.zeros(2)
        if self.enemy:
            direction = self.model.space.get_heading(self.pos, self.enemy.pos)
        return direction
    
    def destroy_enemy(self):
        """
        Destroys the enemy agent and removes said agent from enemy list.
        """
        if self.enemy & (self.model.space.get_distance(self.pos, self.enemy.pos) < vision):
            self.enemy.operability = False # Standardize method
            self.enemy = None
        return True
    
    def step(self):
        """
        Move towards target if target exists.
        """
        if self.enemy:
            self.velocity = self.target_enemy()
            self.velocity /= np.linalg.norm(self.velocity)
            new_pos = self.pos + self.velocity * self.speed
            self.model.space.move_agent(self, new_pos)

            
class REDForce(Agent):
    """
    A REDForce defense agent.
    The agent follows the following behavior:
        - Stationary: Sit in position till destroyed
    """
    
    def __init__(
        self,
        unique_id,
        model,
        pos,
    ):
        """
        Create a new REDForce agent.
        Args:
            unique_id: Unique agent identifyer.
            operability: If the asset is operable
            pos: Starting position
        """
        super().__init__("red_" + str(unique_id), model)
        self.operability = True
        self.pos = np.array(pos)
    
    def step(self):
        """
        Sit still.
        """
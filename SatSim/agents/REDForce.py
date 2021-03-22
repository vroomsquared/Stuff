import numpy as np
import random

from mesa import Agent

            
class REDForce(Agent):
    """
    A REDForce defense agent.
    The agent follows the following behavior:
        - Stationary: Sit in position till destroyed
    
    TODO:
        - Create Disable Function
    """
    
    def __init__( #add color
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
        self.color = "Red"
    
    def isOperable(self):
        return self.operability
    
    def step(self):
        """
        Sit still.
        """
        if not self.operability & (self.color != "Black"):
            self.color = "Black"
import numpy as np
import random

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
    
    def __init__( # add color
        self,
        unique_id,
        model,
        pos,
        speed,
        velocity,
        vision,
        satsystem,
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
        self.color = "Blue"
        
        self.speed = speed
        self.velocity = velocity
        self.vision = vision
        
        self.enemy = None
        self.satsystem = satsystem
        
    def target_enemy(self):
        """
        Return the vector toward the enemy agent.
        """
        threats = self.satsystem.ISR_enemy_agents()
        if threats is not None:
            threats = [e for e in threats if e.isOperable()]
            if threats:
                self.enemy = random.choice(threats)
        
        direction = np.zeros(2)
        if self.enemy:
            direction = self.model.space.get_heading(self.pos, self.enemy.pos)
        return direction
    
    def destroy_enemy(self):
        """
        Destroys the enemy agent and removes said agent from enemy list.
        """
        if (self.model.space.get_distance(self.pos, self.enemy.pos) < self.vision):
            print(self.unique_id + ": target " + self.enemy.unique_id + " within sight") # Debug
            self.enemy.operability = False # Standardize method
            self.enemy = None
        return True
    
    def step(self):
        """
        Move towards target if target exists.
        """
        if (self.enemy is not None): #Fix nested Ifs, TODO
            if self.enemy.isOperable():
                new_pos = self.pos + self.velocity * self.speed
                self.model.space.move_agent(self, new_pos)
                
                self.destroy_enemy() #Results in NAN if misplaced, TODO fix
            else:
                self.velocity = np.random.random(2) * 2 - 1
                self.velocity /= np.linalg.norm(self.velocity)
                new_pos = self.pos + self.velocity * self.speed
                self.model.space.move_agent(self, new_pos)

                self.velocity = self.target_enemy()
                self.velocity /= np.linalg.norm(self.velocity)
        
        else:
            self.velocity = np.random.random(2) * 2 - 1
            self.velocity /= np.linalg.norm(self.velocity)
            new_pos = self.pos + self.velocity * self.speed
            self.model.space.move_agent(self, new_pos)
            
            self.velocity = self.target_enemy()
            self.velocity /= np.linalg.norm(self.velocity)

            
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
            
            
class SatSystem(Agent):
    """
    A Generic Satellite System.
    The agent follows the following behavior:
        - ISR (Main)
        - PNT
        - SatCom
    Sat Systems operate as the environmental observers of the battlefield and observe the
    movements and communications of units (both friendly and enemy).
    """
    
    def __init__( # add color
        self,
        unique_id,
        model,
        success_rate,
        color,
    ):
        """
        Create a new BLUForce agent.
        Args:
            unique_id: Unique agent identifyer.
            operability: If the asset is operable
            color: "Red" or "Blue" for unit specific force.
        """
        super().__init__(("blu_" if color == "Blue" else "red_") + str(unique_id), model)
        self.operability = True
        self.success_rate = success_rate
        self.color = color
        
    def ISR_all_agents(self):
        """
        Return the list of all visible objects from sat system. TODO - add variability
        """
        return self.model.schedule.agents
    
    def ISR_enemy_agents(self):
        """
        Return the list of all enemy objects from sat system. Filter method.
        """
        enemy_agents = self.ISR_all_agents()
        if np.random.random() < self.success_rate:
            enemy_agents = [e for e in enemy_agents if e.color != self.color]
        else:
            enemy_agents = None
        return enemy_agents
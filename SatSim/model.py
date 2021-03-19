import numpy as np

from mesa import Model
from mesa.space import ContinuousSpace
from mesa.time import RandomActivation

from .agents.agent import *

class SCS(Model):
    """
    South China Sea (SCS) model class. Handles agent creation, placement and scheduling.
    """

    def __init__(
        self,
        blu_force=1,
        red_force=1,
        width=100,
        height=100,
        speed=1,
        vision=10,
    ):
        """
        Create a new SCS model.
        Args:
            blu_force: Number of Blue Attack Forces
            red_force: Number of Red Defesne Forces
            width, height: Size of the space.
            speed: How fast should the agents move.
            vision: How far around should each agent look for its enemies
        """
        self.blu_force = blu_force
        self.red_force = red_force
        self.vision = vision
        self.speed = speed
        self.schedule = RandomActivation(self)
        self.space = ContinuousSpace(width, height, False) #Torus: false
        self.make_agents() # Creates Simulation
        self.running = True

    def make_agents(self):
        """
        Create self.***_force agents, with random positions and starting headings.
        """
        blu_sat = SatSystem(
            1,
            self,
            0.1, # Success Rate
            "Blue"
        )
                
        for i in range(self.red_force):
            x_r = self.random.random() * self.space.x_max
            y_r = self.random.random() * self.space.y_max
            pos_r = np.array((x_r, y_r))
            red = REDForce(
                i,
                self,
                pos_r                
            )
            self.space.place_agent(red, pos_r)
            self.schedule.add(red)
            
        for i in range(self.blu_force):
            x_b = self.random.random() * self.space.x_max
            y_b = self.random.random() * self.space.y_max
            pos_b = np.array((x_b, y_b))
            velocity_b = np.random.random(2) * 2 - 1
            blu = BLUForce(
                i,
                self,
                pos_b,
                self.speed,
                velocity_b,
                self.vision,
                blu_sat
            )
            self.space.place_agent(blu, pos_b)
            self.schedule.add(blu)

    def step(self):
        self.schedule.step()
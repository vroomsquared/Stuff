import numpy as np

from mesa import Model
from mesa.space import ContinuousSpace
from mesa.time import RandomActivation

from .agent import BLUForce, REDForce

class SCS(Model):
    """
    South China Sea (SCS) model class. Handles agent creation, placement and scheduling.
    """

    def __init__(
        self,
        population=1,
        width=100,
        height=100,
        speed=1,
        vision=10,
    ):
        """
        Create a new SCS model.
        Args:
            population: Number of Agent pairs
            width, height: Size of the space.
            speed: How fast should the agents move.
            vision: How far around should each agent look for its enemies
        """
        self.population = population
        self.vision = vision
        self.speed = speed
        self.schedule = RandomActivation(self)
        self.space = ContinuousSpace(width, height, True)
        self.make_agents() # Creates Simulation
        self.running = True

    def make_agents(self):
        """
        Create self.population agents, with random positions and starting headings.
        """
        for i in range(self.population):
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
                red
            )
            self.space.place_agent(blu, pos_b)
            self.schedule.add(blu)

    def step(self):
        self.schedule.step()
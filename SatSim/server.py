from mesa.visualization.ModularVisualization import ModularServer

from .model import SCS
from .SimpleContinuousModule import SimpleCanvas


def force_draw(agent):
    return {"Shape": "circle", "r": 2, "Filled": "true", "Color": "Red"}


force_canvas = SimpleCanvas(force_draw, 500, 500)
model_params = {
    "population": 1,
    "width": 100,
    "height": 100,
    "speed": 2,
    "vision": 10,
}

server = ModularServer(SCS, [force_canvas], "Forces", model_params)
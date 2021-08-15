"""Visualizes the cardioid times table
factor increases as the minutes go by
largest number increases as the seconds go by
"""
import math
from datetime import datetime

import numpy as np
import scene
import scene_drawing


screen_width, screen_height = scene.get_screen_size()
centerx, centery = scene.get_screen_size() / 2


def factorpoints(radius, factor, maxnum):
    """Returns the coordinates of the lines in the cardioid defined by the factor and the maximum number
    Returns lines as (x1,y1,x2,y2)
    """
    maxnum += 1
    twopi = 2 * math.pi
    d_radian = twopi / maxnum
    radian = 0
    while radian < twopi:
        x1 = centerx + radius * math.cos(radian)
        y1 = centery + radius * math.sin(radian)
        radian2 = radian * factor % maxnum
        x2 = centerx + radius * math.cos(radian2)
        y2 = centery + radius * math.sin(radian2)
        radian += d_radian
        yield x1, y1, x2, y2


class Main(scene.Scene):
    def setup(self):
        self.background_color = 'black'
        self.radius = centerx
        timestamp = datetime.now()
        self.time = timestamp.minute * 60
        + timestamp.second
        + timestamp.microsecond // 10000 % 60 / 60

    def getfactors(self):
        """Calculates factor, maxnum, and increments self.time"""
        sixtieth = 1 / 60
        inverse120pi = 1 / (2 * math.pi) * sixtieth
        minutehand = self.time * sixtieth
        # oscillates seconds between 0 and 60
        # if i did self.time % 60, then there would be an awkward jump every minute
        secondhand = 60 + 60 * math.cos(self.time / (2 * math.pi))
        # arbitrarynum is a number i think makes the graph look better
        arbitrarynum = 100
        factor = arbitrarynum * math.sin(minutehand * inverse120pi)
        # have to add arbitrarynum so maxnum is never < 0
        maxnum = arbitrarynum + arbitrarynum * math.cos(secondhand * inverse120pi)
        self.time += sixtieth
        return factor, maxnum

    def draw(self):
        # scene_drawing.ellipse uses diameter for its width and height function
        # also its x, y is at the bottom-left, not center
        scene_drawing.no_fill()
        scene_drawing.stroke(1, 1, 1)
        scene_drawing.stroke_weight(0.5)
        scene_drawing.ellipse(centerx - self.radius, centery - self.radius, self.radius * 2, self.radius * 2)
        factor, maxnum = self.getfactors()
        for line in factorpoints(self.radius, factor, maxnum):
            scene_drawing.line(*line)


if __name__ == '__main__':
    scene.run(Main())


from math import cos, pi, sin
from typing import List

import numpy as np

from networks.geometry.Point2D import Point2D


class Circle:
    def __init__(self, center: Point2D):
        self.center = center

        self.radius = None
        self.points: List[Point2D] = []

        self.inner = None
        self.outer = None
        self.points_thick: List[Point2D] = []

        self.spaced_radius = None
        self.spaced_points: List[Point2D] = []

    def __repr__(self):
        return f"Circle(center: {self.center}, radius: {self.radius}, spaced_radius: {self.spaced_radius}, inner: {self.inner}, outer: {self.outer})"

    def circle(self, radius: int) -> List[Point2D]:
        self.radius = radius
        center = self.center.copy()

        x = -radius
        y = 0
        error = 2-2*radius
        while (True):
            self.points.append(Point2D(center.x-x, center.y+y))
            self.points.append(Point2D(center.x-y, center.y-x))
            self.points.append(Point2D(center.x+x, center.y-y))
            self.points.append(Point2D(center.x+y, center.y+x))
            r = error
            if (r <= y):
                y += 1
                error += y*2+1
            if (r > x or error > y):
                x += 1
                error += x*2+1
            if (x < 0):
                continue
            else:
                break
        return self.points

    def circle_thick(self, inner: int, outer: int) -> List[Point2D]:
        """Compute discrete value of a 2d-circle with thickness. 

        From: https://stackoverflow.com/questions/27755514/circle-with-thickness-drawing-algorithm

        Args:
            inner (int): The minimum radius at which the disc is filled (included).
            outer (int): The maximum radius where disc filling stops (included).

        Returns:
            list(Point2D): List of 2d-coordinates composing the surface. Note that some coordinates are redondant and are not ordered.

        >>> Circle(Point2D(0, 0), 5, 10)
        """

        self.inner = inner
        self.outer = outer
        center = self.center.copy()

        xo = outer
        xi = inner

        y = 0
        erro = 1 - xo
        erri = 1 - xi

        while xo >= y:
            self._x_line(center.x + xi, center.x + xo, center.y + y)
            self._y_line(center.x + y,  center.y + xi, center.y + xo)
            self._x_line(center.x - xo, center.x - xi, center.y + y)
            self._y_line(center.x - y,  center.y + xi, center.y + xo)
            self._x_line(center.x - xo, center.x - xi, center.y - y)
            self._y_line(center.x - y,  center.y - xo, center.y - xi)
            self._x_line(center.x + xi, center.x + xo, center.y - y)
            self._y_line(center.x + y,  center.y - xo, center.y - xi)

            y += 1

            if erro < 0:
                erro += 2 * y + 1
            else:
                xo -= 1
                erro += 2 * (y - xo + 1)

            if y > inner:
                xi = y
            else:
                if erri < 0:
                    erri += 2 * y + 1
                else:
                    xi -= 1
                    erri += 2 * (y - xi + 1)
        return self.points_thick

    def circle_spaced(self, number: int, radius: int) -> List[Point2D]:
        """Get evenly spaced coordinates of the circle.

        From: https://stackoverflow.com/questions/8487893/generate-all-the-points-on-the-circumference-of-a-circle

        Args:
            number (int): Number of coordinates to be returned. 
            radius (int): Radius of the circle.

        Returns:
            list(Point2D): List of evenly spaced 2d-coordinates forming the circle.
        """
        self.spaced_radius = radius
        center = self.center

        self.spaced_points = [
            Point2D(round(cos(2 * pi / number * i) * radius),
                    round(sin(2 * pi / number * i) * radius))
            for i in range(0, number + 1)
        ]

        for i in range(len(self.spaced_points)):
            current_point = Point2D(
                self.spaced_points[i].x + center.x,
                self.spaced_points[i].y + center.y
            ).round()
            self.spaced_points[i] = current_point
        return self.spaced_points

    def _x_line(self, x1, x2, y):
        while x1 <= x2:
            self.points_thick.append(Point2D(x1, y))
            x1 += 1

    def _y_line(self, x, y1, y2):
        while y1 <= y2:
            self.points_thick.append(Point2D(x, y1))
            y1 += 1

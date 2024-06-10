from typing import Type
import Point2D


class Circle:
    def __init__(center: Type[Point2D], inner: int, outer: int):
        self.center = center
        self.inner = inner
        self.outer = outer
        self.coordinates = []

        circle(self.center, self.inner, self.outer)

    def circle(center: Type[Point2D], inner: int, outer: int):
        """Compute discrete value of a 2d-circle with thickness. 

        https://stackoverflow.com/questions/27755514/circle-with-thickness-drawing-algorithm

        Args:
            center (Type[Point2D]): Center of the circle. Circles always have an odd diameter due to the central coordinate.
            inner (int): The minimum radius at which the disc is filled (included).
            outer (int): The maximum radius where disc filling stops (included).
        """
        xo = outer
        xi = inner
        y = 0
        erro = 1 - xo
        erri = 1 - xi

        while xo >= y:
            _x_line(center.x + xi, center.x + xo, center.y + y)
            _y_line(center.x + y,  center.y + xi, center.y + xo)
            _x_line(center.x - xo, center.x - xi, center.y + y)
            _y_line(center.x - y,  center.y + xi, center.y + xo)
            _x_line(center.x - xo, center.x - xi, center.y - y)
            _y_line(center.x - y,  center.y - xo, center.y - xi)
            _x_line(center.x + xi, center.x + xo, center.y - y)
            _y_line(center.x + y,  center.y - xo, center.y - xi)

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

    def _x_line(x1, x2, y):
        while x1 <= x2:
            self.coordinates.append(Point2D(x1, y))
            x1 += 1

    def _y_line(x, y1, y2):
        while y1 <= y2:
            self.coordinate.append(Point2D(x, y1))
            y1 += 1

    def __repr__(self):
        return f"Circle(center: {self.center}, inner: {self.inner}, outer: {self.outer})"

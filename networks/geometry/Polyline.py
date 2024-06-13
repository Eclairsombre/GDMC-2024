from networks.geometry.Point2D import Point2D

from math import sqrt, inf
import numpy as np


class Polyline:
    def __init__(self, points: list["Point2D"]):
        """A polyline with smooth corners, only composed of segments and circle arc.

        Mathematics and algorithms behind this can be found here: https://cdr.lib.unc.edu/concern/dissertations/pz50gw814?locale=en, E2 Construction of arc roads from polylines, page 210.

        Args:
            points (List[Point2D]): List of 2d-points in order describing the polyline.

        Raises:
            ValueError: At least 4 points required.

        >>> Polyline((Point2D(0, 0), Point2D(0, 10), Point2D(50, 10), Point2D(20, 20)))
        """
        self.points_array = Point2D.to_vectors(
            self._remove_collinear_points(points))
        self.length_polyline = len(self.points_array)

        if self.length_polyline < 4:
            raise ValueError("The list must contain at least 4 elements.")

        self.vectors = [None] * self.length_polyline  # v
        self.lengths = [None] * (self.length_polyline - 1)  # l
        self.unit_vectors = [None] * self.length_polyline  # n
        self.tangente = [0] * self.length_polyline  # f

        # alpha, maximum radius factor
        self.alpha_radii = [None] * self.length_polyline

        self.radii = [None] * self.length_polyline  # r
        self.centers = [None] * self.length_polyline  # c
        self.acrs_intersections = [None] * self.length_polyline

        self._compute_requirements()
        self._compute_alpha_radii()

        self._alpha_assign(0, self.length_polyline-1)

        self.output_points = points

    def __repr__(self):
        return str(self.alpha_radii)

    def get_radii(self):
        for i in range(1, self.length_polyline-1):
            self.radii[i] = round(self.alpha_radii[i] * self.tangente[i])
        return self.radii

    def get_centers(self):
        if self.radii == [None] * self.length_polyline:
            raise ValueError("No radii found. Run get_radii before.")

        for i in range(1, self.length_polyline-1):
            bisector = (self.unit_vectors[i] - self.unit_vectors[i-1]) / (
                np.linalg.norm(self.unit_vectors[i] - self.unit_vectors[i-1]))

            array = self.points_array[i] + sqrt((self.radii[i]
                                                 ** 2) + (self.alpha_radii[i] ** 2)) * bisector
            self.centers[i] = Point2D(array[0], array[1]).round()
        return self.centers

    def get_arcs_intersections(self):
        for i in range(1, self.length_polyline-1):
            point_1 = self.points_array[i] - \
                self.alpha_radii[i] * self.unit_vectors[i-1]
            point_2 = self.points_array[i] + \
                self.alpha_radii[i] * self.unit_vectors[i]
            self.acrs_intersections[i] = Point2D(
                point_1[0], point_1[1]).round(), Point2D(self.points_array[i][0], self.points_array[i][1]), Point2D(point_2[0], point_2[1]).round()
        return self.acrs_intersections

    def _alpha_assign(self, start_index: int, end_index: int):
        """
        The alpha-assign procedure assigning radii based on a polyline.
        """
        minimum_radius, minimum_index = inf, end_index

        if start_index + 1 >= end_index:
            return

        alpha_b = min(
            self.lengths[start_index] - self.alpha_radii[start_index], self.lengths[start_index + 1])
        current_radius = max(self.tangente[start_index] * self.alpha_radii[start_index],
                             self.tangente[start_index + 1] * alpha_b)  # Radius at initial segment

        if current_radius < minimum_radius:
            minimum_radius, minimum_index = current_radius, start_index
            # 0, 8
            alpha_low, alpha_high = self.alpha_radii[start_index], alpha_b

        for i in range(start_index + 1, end_index - 1):  # Radii for internal segments
            alpha_a, alpha_b, current_radius = self._radius_balance(i)

            if current_radius < minimum_radius:
                minimum_radius, minimum_index = current_radius, i
                alpha_low, alpha_high = alpha_a, alpha_b

        alpha_a = min(self.lengths[end_index-2],
                      self.lengths[end_index-1]-self.alpha_radii[end_index])

        current_radius = max(self.tangente[end_index-1]*alpha_a, self.tangente[end_index]
                             * self.alpha_radii[end_index])  # Radius at final segment

        if current_radius < minimum_radius:
            minimum_radius, minimum_index = current_radius, end_index - 1
            alpha_low, alpha_high = alpha_a, self.alpha_radii[end_index]

        # Assign alphas at ends of selected segment
        self.alpha_radii[minimum_index] = alpha_low
        self.alpha_radii[minimum_index+1] = alpha_high
        # Recur on lower segments
        self._alpha_assign(start_index, minimum_index)
        # Recur on higher segments
        self._alpha_assign(minimum_index + 1, end_index)

    def _radius_balance(self, i: int):
        """
        Returns the radius that balances the radii on either end segement i.
        """

        alpha_a = min(self.lengths[i-1], (self.lengths[i]*self.tangente[i+1]) /
                      (self.tangente[i] + self.tangente[i+1]))
        alpha_b = min(self.lengths[i+1], self.lengths[i]-alpha_a)
        return alpha_a, alpha_b, min(self.tangente[i]*alpha_a, self.tangente[i+1]*alpha_b)

    def _compute_requirements(self):
        # Between two points, there is only one segment
        for j in range(self.length_polyline-1):
            self.vectors[j] = self.points_array[j+1] - self.points_array[j]
            self.lengths[j] = np.linalg.norm(self.vectors[j])
            self.unit_vectors[j] = self.vectors[j]/self.lengths[j]

        # Between two segments, there is only one angle
        for k in range(1, self.length_polyline-1):
            dot = np.dot(self.unit_vectors[k], self.unit_vectors[k-1])
            self.tangente[k] = sqrt((1+dot)/(1-dot))

    def _compute_alpha_radii(self):
        self.alpha_radii[0] = 0
        self.alpha_radii[self.length_polyline-1] = 0

    @staticmethod
    def _remove_collinear_points(points):
        output_points = [points[0]]

        for i in range(1, len(points) - 1):
            if not Point2D.collinear(
                    points[i-1], points[i], points[i+1]):
                output_points.append(points[i])

        output_points.append(points[-1])
        return output_points

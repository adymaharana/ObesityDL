class Point:
    def __init__(self, x, y):
        """
        A point specified by (x,y) coordinates in the cartesisan place
        """
        self.x = x
        self.y = y

class Polygon:
    def __init__(self, points):
        """
        points: a list of points in clockwise order
        """
        self.points = points

    @property
    def edges(self):
        ''' Returns a list of tuples that each contain 2 points of an edge'''
        edge_list = []
        for i,p in enumerate(self.points):
            p1 = p
            p2 = self.points[(i-1) % len(self.points)]
            edge_list.append((p1,p2))

        return edge_list

    def contains(self, point):
        import sys
        # _huge is used to act as infinity if we divide by 0
        _huge = sys.float_info.max
        # eps is ised to make sure points are not on the same line as vertexes
        _eps = 0.00001

        # Start on the outside of the polygon
        inside = False
        for edge in self.edges:
            # make sure A is the lower point of edge
            A, B = edge[0], edge[1]
            if A.y > B.y:
                A, B = B, A

            # make sure point is not same height as vertex
            if point.y == A.y or point.y == B.y:
                point.y += _eps

            if (point.y > B.y or point.y < A.y or point.x > max(A.x, B.x)):
                # horizontal ray does not intersect with edge
                continue

            if point.x < min(A.x, B.x):
                # ray intersects with edge
                inside = not inside
                continue

            try:
                m_edge = (B.y - A.y) / (B.x - A.x)
            except ZeroDivisionError:
                m_edge = _huge

            try:
                m_point = (point.y - A.y) / (point.x - A.x)
            except ZeroDivisionError:
                m_point = _huge

            if m_point >= m_edge:
                # ray intersects with edge:
                inside = not inside
                continue
        return inside
    
if __name__ == "__main__":
    
    q = Polygon([Point(20,10), Point(50,125), Point(125,90), Point(150,10)])
    # Test 1: Point inside of polygon
    p1 = Point(75,50)
    print("P1 inside polygon: " + str(q.contains(p1)))

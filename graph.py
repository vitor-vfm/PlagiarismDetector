import random
import collections

class Graph:
    """
    Directed Graph Class
    Created by UofAlberta CMPUT 275 instructors
    Changed to have weighted edges
    
    A graph is modelled as a dictionary that maps a vertex
    to the list of neighbours of that vertex.

    There is a dictionary that maps edges to their weights
    
    From the Jan 22/23 lectures.
    """

    def __init__(self, vertices = set(), edges = list(), weights = list()):
        """
        Construct a graph with a shallow copy of
        the given set of vertices and given list of edges.

        Efficiency: O(# vertices + # edges)

        >>> g = Graph({1,2,3}, [(1,2), (2,3)], [3,4])
        >>> g._alist.keys() == {1,2,3}
        True
        >>> g._alist[1] == [2]
        True
        >>> g._alist[2] == [3]
        True
        >>> g._alist[3] == []
        True
        >>> h1 = Graph()
        >>> h2 = Graph()
        >>> h1.add_vertex(1)
        >>> h2._alist.keys() == set()
        True
        """

        self._alist = dict()
        self._edges = dict()

        for v in vertices:
            self.add_vertex(v)
        for i, e in enumerate(edges):
            self.add_edge(e, weights[i])

    def add_vertex(self, v):
        """
        Add a vertex v to the graph.
        If v exists in the graph, do nothing.

        Efficiency: O(1)

        >>> g = Graph()
        >>> len(g._alist)
        0
        >>> g.add_vertex(1)
        >>> g.add_vertex("vertex")
        >>> "vertex" in g._alist
        True
        >>> 2 in g._alist
        False
        >>> h = Graph({1,2}, [(1,2)], [3])
        >>> h.add_vertex(1)
        >>> h._alist[1] == [2]
        True
        """
        
        if v not in self._alist:
            self._alist[v] = list()

    def add_edge(self, e, w):
        """
        Add edge e to the graph.
        Raise an exception if the endpoints of
        e are not in the graph.

        Efficiency: O(1)

        >>> g = Graph()
        >>> g.add_vertex(1)
        >>> g.add_vertex(2)
        >>> g.add_edge((1,2), 3)
        >>> 2 in g._alist[1]
        True
        >>> 1 in g._alist[2]
        False
        >>> g.add_edge((1,2), 4)
        >>> g._alist[1] == [2,2]
        True
        """

        if not self.is_vertex(e[0]) \
          or not self.is_vertex(e[1]):
            raise ValueError("an endpoint is not in graph")

        self._alist[e[0]].append(e[1])
        self._edges[e] = w

    def is_vertex(self, v):
        """
        Check if vertex v is in the graph.
        Return True if it is, False if it is not.
        
        Efficiency: O(1) - Sweeping some discussion
        about hashing under the rug.

        >>> g = Graph({1,2})
        >>> g.is_vertex(1)
        True
        >>> g.is_vertex(3)
        False
        >>> g.add_vertex(3)
        >>> g.is_vertex(3)
        True
        """
        return v in self._alist

    def is_edge(self, e):
        """
        Check if edge e is in the graph.
        Return True if it is, False if it is not.

        Efficiency: O(# neighbours of e[0])

        >>> g = Graph({1,2}, [(1,2)], [5])
        >>> g.is_edge((1,2))
        True
        >>> g.is_edge((2,1))
        False
        >>> g.add_edge((1,2), 5)
        >>> g.is_edge((1,2))
        True
        """

        if e[0] not in self._alist:
            return False
        else:
            return e[1] in self._alist[e[0]]

    def neighbours(self, v):
        """
        Return a list of neighbours of v.
        A vertex u appears in this list as many
        times as the (v,u) edge is in the graph.

        If v is not in the graph, then
        raise a ValueError exception.

        Efficiency: O(1)

        >>> Edges = [(1,2),(1,4),(3,1),(3,4),(2,4),(1,2)]
        >>> Weights = [2,4,5,1,2,3]
        >>> g = Graph({1,2,3,4}, Edges, Weights)
        >>> g.neighbours(1)
        [2, 4, 2]
        >>> g.neighbours(4)
        []
        >>> g.neighbours(3)
        [1, 4]
        >>> g.neighbours(2)
        [4]
        """

        if not self.is_vertex(v):
            raise ValueError("vertex not in graph")
        
        return self._alist[v]

    def vertices(self):
        """
        Returns the set of vertices in the graph.

        Efficiency: O(# vertices)

        >>> g = Graph({1,2})
        >>> g.vertices() == {1,2}
        True
        >>> g.add_vertex(3)
        >>> g.vertices() == {1,2,3}
        True
        """

        # dict.keys() is not exactly a set, so we have to create
        # one before returning
        return set(self._alist.keys()) 

    def edges(self):
        """
        Returns the edges dictionary
        """
        return self._edges

    def get_edge_weight(self, e):
        """
        >>> g = Graph({1,2})
        >>> g.add_edge((1,2), 4)
        >>> g.get_edge_weight((1,2))
        4
        """
        return self._edges[e]


#END OF CLASS DEFINITION

if __name__=="__main__":
    import doctest
    doctest.testmod()

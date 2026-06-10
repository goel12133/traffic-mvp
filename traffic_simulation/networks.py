from itertools import pairwise


class Network:
    def __init__(self, edges, routes):
        self.edges = edges
        self.routes = routes

    def route_edges(self, route_name):
        return list(pairwise(self.routes[route_name]))

    def empty_edge_counts(self):
        return {edge: 0 for edge in self.edges}

    def empty_route_counts(self):
        return {route_name: 0 for route_name in self.routes}

    def edge_time(self, edge, cars_on_edge):
        road = self.edges[edge]
        return road["base_time"] + road["congestion"] * cars_on_edge

    def route_time(self, route_name, edge_counts):
        total_time = 0
        for edge in self.route_edges(route_name):
            total_time += self.edge_time(edge, edge_counts[edge])
        return total_time

    def build_edge_counts(self, route_counts):
        edge_counts = self.empty_edge_counts()
        for route_name, cars_on_route in route_counts.items():
            for edge in self.route_edges(route_name):
                edge_counts[edge] += cars_on_route
        return edge_counts


TWO_ROUTE_NETWORK = Network(
    edges={
        ("A", "B"): {"base_time": 10, "congestion": 0.20},
        ("B", "D"): {"base_time": 0, "congestion": 0.00},
        ("A", "C"): {"base_time": 12, "congestion": 0.03},
        ("C", "D"): {"base_time": 0, "congestion": 0.00},
    },
    routes={
        "short_low_capacity": ["A", "B", "D"],
        "long_high_capacity": ["A", "C", "D"],
    },
)

BRAESS_NETWORK = Network(
    edges={
        ("A", "B"): {"base_time": 0, "congestion": 1.00},
        ("B", "D"): {"base_time": 45, "congestion": 0.00},
        ("A", "C"): {"base_time": 45, "congestion": 0.00},
        ("C", "D"): {"base_time": 0, "congestion": 1.00},
        ("B", "C"): {"base_time": 0, "congestion": 0.00},
    },
    routes={
        "top": ["A", "B", "D"],
        "bottom": ["A", "C", "D"],
        "shortcut": ["A", "B", "C", "D"],
    },
)

BRAESS_NETWORK_WITHOUT_SHORTCUT = Network(
    edges={
        ("A", "B"): {"base_time": 0, "congestion": 1.00},
        ("B", "D"): {"base_time": 45, "congestion": 0.00},
        ("A", "C"): {"base_time": 45, "congestion": 0.00},
        ("C", "D"): {"base_time": 0, "congestion": 1.00},
    },
    routes={
        "top": ["A", "B", "D"],
        "bottom": ["A", "C", "D"],
    },
)

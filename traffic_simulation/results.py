class SimulationResult:
    def __init__(self, route_counts, edge_counts, route_times, average_time):
        self.route_counts = route_counts
        self.edge_counts = edge_counts
        self.route_times = route_times
        self.average_time = average_time


def build_result(network, route_counts, num_drivers):
    edge_counts = network.build_edge_counts(route_counts)
    route_times = {
        route_name: round(network.route_time(route_name, edge_counts), 2)
        for route_name in network.routes
    }
    average_time = round(_average_time(network, route_counts, num_drivers), 2)
    return SimulationResult(route_counts, edge_counts, route_times, average_time)


def _average_time(network, route_counts, num_drivers):
    edge_counts = network.build_edge_counts(route_counts)
    total_time = sum(
        network.route_time(route_name, edge_counts) * cars_on_route
        for route_name, cars_on_route in route_counts.items()
    )
    return total_time / num_drivers


def price_of_anarchy(selfish_result, optimal_result):
    return round(selfish_result.average_time / optimal_result.average_time, 
                 

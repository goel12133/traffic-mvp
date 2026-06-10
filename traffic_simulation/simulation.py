import random

from traffic_simulation.results import build_result, _average_time


ADOPTION_RATE_MIN = 0
ADOPTION_RATE_MAX = 100
ADOPTION_RATE_STEP = 10


def simulate_random(network, num_drivers):
    route_counts = network.empty_route_counts()
    route_names = list(network.routes)

    for _ in range(num_drivers):
        route_name = random.choice(route_names)
        route_counts[route_name] += 1

    return build_result(network, route_counts, num_drivers)


def simulate_naive_selfish(network, num_drivers):
    route_counts = network.empty_route_counts()
    edge_counts = network.empty_edge_counts()

    best_route = min(
        network.routes,
        key=lambda route_name: network.route_time(route_name, edge_counts),
    )
    route_counts[best_route] = num_drivers

    return build_result(network, route_counts, num_drivers)


def simulate_sequential_selfish(network, num_drivers):
    route_counts = network.empty_route_counts()

    for _ in range(num_drivers):
        edge_counts = network.build_edge_counts(route_counts)

        best_route = min(
            network.routes,
            key=lambda route_name: network.route_time(route_name, edge_counts),
        )
        route_counts[best_route] += 1

    return build_result(network, route_counts, num_drivers)


def simulate_system_optimal_greedy(network, num_drivers):
    route_counts = network.empty_route_counts()

    for _ in range(num_drivers):
        best_route = min(
            network.routes,
            key=lambda route_name: _marginal_average_time(network, route_counts, route_name, num_drivers),
        )
        route_counts[best_route] += 1

    return build_result(network, route_counts, num_drivers)


def simulate_partial_adoption(network, num_drivers, adoption_rate):
    route_counts = network.empty_route_counts()
    route_names = list(network.routes)

    for _ in range(num_drivers):
        is_app_user = random.random() < adoption_rate

        if is_app_user:
            edge_counts = network.build_edge_counts(route_counts)
            best_route = min(
                network.routes,
                key=lambda route_name: network.route_time(route_name, edge_counts),
            )
        else:
            best_route = random.choice(route_names)

        route_counts[best_route] += 1

    return build_result(network, route_counts, num_drivers)


def _marginal_average_time(network, route_counts, route_name, num_drivers):
    trial_counts = route_counts.copy()
    trial_counts[route_name] += 1
    return _average_time(network, trial_counts, num_drivers)

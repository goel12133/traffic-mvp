import random
from itertools import pairwise

NUM_DRIVERS = 100
RANDOM_SEED = 42


TWO_ROUTE_NETWORK = {
    "edges": {
        ("A", "B"): {"base_time": 10, "congestion": 0.20},
        ("B", "D"): {"base_time": 0, "congestion": 0.00},
        ("A", "C"): {"base_time": 12, "congestion": 0.03},
        ("C", "D"): {"base_time": 0, "congestion": 0.00},
    },
    "routes": {
        "short_low_capacity": ["A", "B", "D"],
        "long_high_capacity": ["A", "C", "D"],
    },
}


BRAESS_NETWORK = {
    "edges": {
        ("A", "B"): {"base_time": 0, "congestion": 1.00},
        ("B", "D"): {"base_time": 45, "congestion": 0.00},
        ("A", "C"): {"base_time": 45, "congestion": 0.00},
        ("C", "D"): {"base_time": 0, "congestion": 1.00},
        ("B", "C"): {"base_time": 0, "congestion": 0.00},
    },
    "routes": {
        "top": ["A", "B", "D"],
        "bottom": ["A", "C", "D"],
        "shortcut": ["A", "B", "C", "D"],
    },
}


BRAESS_WITHOUT_SHORTCUT = {
    "edges": {
        ("A", "B"): {"base_time": 0, "congestion": 1.00},
        ("B", "D"): {"base_time": 45, "congestion": 0.00},
        ("A", "C"): {"base_time": 45, "congestion": 0.00},
        ("C", "D"): {"base_time": 0, "congestion": 1.00},
    },
    "routes": {
        "top": ["A", "B", "D"],
        "bottom": ["A", "C", "D"],
    },
}


def get_route_edges(route):
    return list(pairwise(route))


def empty_edge_counts(network):
    return {edge: 0 for edge in network["edges"]}


def empty_route_counts(network):
    return {route_name: 0 for route_name in network["routes"]}


def edge_time(network, edge, cars_on_edge):
    road = network["edges"][edge]
    return road["base_time"] + road["congestion"] * cars_on_edge


def route_time(network, route_name, edge_counts):
    route = network["routes"][route_name]
    total_time = 0

    for edge in get_route_edges(route):
        total_time += edge_time(network, edge, edge_counts[edge])

    return total_time


def build_edge_counts(network, route_counts):
    edge_counts = empty_edge_counts(network)

    for route_name, cars_on_route in route_counts.items():
        route = network["routes"][route_name]

        for edge in get_route_edges(route):
            edge_counts[edge] += cars_on_route

    return edge_counts


def calculate_average_time(network, route_counts):
    edge_counts = build_edge_counts(network, route_counts)
    total_time = 0

    for route_name, cars_on_route in route_counts.items():
        total_time += route_time(network, route_name, edge_counts) * cars_on_route

    return total_time / NUM_DRIVERS


def calculate_result(network, route_counts):
    edge_counts = build_edge_counts(network, route_counts)
    route_times = {}

    for route_name in network["routes"]:
        route_times[route_name] = round(route_time(network, route_name, edge_counts), 2)

    return {
        "route_counts": route_counts,
        "edge_counts": edge_counts,
        "route_times": route_times,
        "average_time": round(calculate_average_time(network, route_counts), 2),
    }


def simulate_random(network):
    route_counts = empty_route_counts(network)
    route_names = list(network["routes"])

    for _ in range(NUM_DRIVERS):
        route_name = random.choice(route_names)
        route_counts[route_name] += 1

    return calculate_result(network, route_counts)


def simulate_naive_selfish(network):
    route_counts = empty_route_counts(network)
    edge_counts = empty_edge_counts(network)

    best_route = min(
        network["routes"],
        key=lambda route_name: route_time(network, route_name, edge_counts),
    )

    route_counts[best_route] = NUM_DRIVERS

    return calculate_result(network, route_counts)


def simulate_sequential_selfish(network):
    route_counts = empty_route_counts(network)

    for _ in range(NUM_DRIVERS):
        edge_counts = build_edge_counts(network, route_counts)

        best_route = min(
            network["routes"],
            key=lambda route_name: route_time(network, route_name, edge_counts),
        )

        route_counts[best_route] += 1

    return calculate_result(network, route_counts)


def simulate_system_optimal_greedy(network):
    route_counts = empty_route_counts(network)

    for _ in range(NUM_DRIVERS):
        best_route = None
        best_average_time = float("inf")

        for route_name in network["routes"]:
            trial_counts = route_counts.copy()
            trial_counts[route_name] += 1
            trial_average_time = calculate_average_time(network, trial_counts)

            if trial_average_time < best_average_time:
                best_average_time = trial_average_time
                best_route = route_name

        route_counts[best_route] += 1

    return calculate_result(network, route_counts)


def simulate_partial_adoption(network, adoption_rate):
    route_counts = empty_route_counts(network)
    route_names = list(network["routes"])

    for _ in range(NUM_DRIVERS):
        uses_routing_app = random.random() < adoption_rate

        if uses_routing_app:
            edge_counts = build_edge_counts(network, route_counts)

            best_route = min(
                network["routes"],
                key=lambda route_name: route_time(network, route_name, edge_counts),
            )
        else:
            best_route = random.choice(route_names)

        route_counts[best_route] += 1

    return calculate_result(network, route_counts)


def price_of_anarchy(selfish_result, optimal_result):
    return round(selfish_result["average_time"] / optimal_result["average_time"], 3)


def print_result(strategy_name, result):
    print(strategy_name)
    print(f"  Route counts: {result['route_counts']}")
    print(f"  Route times:  {result['route_times']}")
    print(f"  Average time: {result['average_time']}")
    print()


def run_strategy_comparison(title, network):
    print("=" * 70)
    print(title)
    print("=" * 70)

    random_result = simulate_random(network)
    naive_result = simulate_naive_selfish(network)
    sequential_result = simulate_sequential_selfish(network)
    optimal_result = simulate_system_optimal_greedy(network)

    print_result("Random routing", random_result)
    print_result("Naive selfish routing", naive_result)
    print_result("Sequential selfish routing", sequential_result)
    print_result("System-optimal greedy routing", optimal_result)

    print(f"Price of Anarchy: {price_of_anarchy(sequential_result, optimal_result)}")
    print()


def run_adoption_experiment(title, network):
    print("=" * 70)
    print(title)
    print("=" * 70)

    print("Adoption rate | Average time | Route counts")
    print("--------------------------------------------")

    for adoption_percent in range(0, 110, 10):
        adoption_rate = adoption_percent / 100
        result = simulate_partial_adoption(network, adoption_rate)

        print(
            f"{adoption_percent:>12}% | "
            f"{result['average_time']:>12} | "
            f"{result['route_counts']}"
        )

    print()


def compare_braess_shortcut():
    print("=" * 70)
    print("Braess comparison: before and after adding shortcut")
    print("=" * 70)

    without_shortcut = simulate_sequential_selfish(BRAESS_WITHOUT_SHORTCUT)
    with_shortcut = simulate_sequential_selfish(BRAESS_NETWORK)

    print_result("Without shortcut", without_shortcut)
    print_result("With shortcut", with_shortcut)

    difference = round(
        with_shortcut["average_time"] - without_shortcut["average_time"],
        2,
    )

    print(f"Change after adding shortcut: {difference}")
    print()


def main():
    random.seed(RANDOM_SEED)

    print("TRAFFIC ROUTING MVP DEMO")
    print("Question: Can individually optimal routing hurt total traffic flow?")
    print()

    run_strategy_comparison(
        "Experiment 1: Two-route congestion network",
        TWO_ROUTE_NETWORK,
    )

    run_strategy_comparison(
        "Experiment 2: Braess-style network with shortcut",
        BRAESS_NETWORK,
    )

    compare_braess_shortcut()

    run_adoption_experiment(
        "Experiment 3: Adoption rate experiment",
        TWO_ROUTE_NETWORK,
    )


if __name__ == "__main__":
    main()

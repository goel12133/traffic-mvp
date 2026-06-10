from traffic_simulation.results import price_of_anarchy
from traffic_simulation.simulation import (
    ADOPTION_RATE_MIN,
    ADOPTION_RATE_MAX,
    ADOPTION_RATE_STEP,
    simulate_naive_selfish,
    simulate_partial_adoption,
    simulate_random,
    simulate_sequential_selfish,
    simulate_system_optimal_greedy,
)

SEPARATOR_WIDTH = 70
SEPARATOR = "=" * SEPARATOR_WIDTH


def print_result(strategy_name, result):
    print(strategy_name)
    print(f"  Route counts: {result.route_counts}")
    print(f"  Route times:  {result.route_times}")
    print(f"  Average time: {result.average_time}")
    print()


def run_strategy_comparison(title, network, num_drivers):
    print(SEPARATOR)
    print(title)
    print(SEPARATOR)

    random_result = simulate_random(network, num_drivers)
    naive_result = simulate_naive_selfish(network, num_drivers)
    sequential_result = simulate_sequential_selfish(network, num_drivers)
    optimal_result = simulate_system_optimal_greedy(network, num_drivers)

    print_result("Random routing", random_result)
    print_result("Naive selfish routing", naive_result)
    print_result("Sequential selfish routing", sequential_result)
    print_result("System-optimal greedy routing", optimal_result)

    print(f"Price of Anarchy: {price_of_anarchy(sequential_result, optimal_result)}")
    print()


def run_adoption_experiment(title, network, num_drivers):
    print(SEPARATOR)
    print(title)
    print(SEPARATOR)

    print("Adoption rate | Average time | Route counts")
    print("-" * SEPARATOR_WIDTH)

    for adoption_percent in range(ADOPTION_RATE_MIN, ADOPTION_RATE_MAX + ADOPTION_RATE_STEP, ADOPTION_RATE_STEP):
        adoption_rate = adoption_percent / 100
        result = simulate_partial_adoption(network, num_drivers, adoption_rate)

        print(
            f"{adoption_percent:>12}% | "
            f"{result.average_time:>12} | "
            f"{result.route_counts}"
        )

    print()


def compare_braess_shortcut(network_without_shortcut, network_with_shortcut, num_drivers):
    print(SEPARATOR)
    print("Braess comparison: before and after adding shortcut")
    print(SEPARATOR)

    without_shortcut = simulate_sequential_selfish(network_without_shortcut, num_drivers)
    with_shortcut = simulate_sequential_selfish(network_with_shortcut, num_drivers)

    print_result("Without shortcut", without_shortcut)
    print_result("With shortcut", with_shortcut)

    difference = round(with_shortcut.average_time - without_shortcut.average_time, 2)
    print(f"Change after adding shortcut: {difference}")
    print()
    

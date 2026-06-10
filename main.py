import random

from traffic_simulation.networks import (
    BRAESS_NETWORK,
    BRAESS_NETWORK_WITHOUT_SHORTCUT,
    TWO_ROUTE_NETWORK,
)
from traffic_simulation.reporting import (
    compare_braess_shortcut,
    run_adoption_experiment,
    run_strategy_comparison,
)

NUM_DRIVERS = 100
RANDOM_SEED = 42


def main():
    random.seed(RANDOM_SEED)

    print("TRAFFIC ROUTING MVP DEMO")
    print("Question: Can individually optimal routing hurt total traffic flow?")
    print()

    run_strategy_comparison(
        "Experiment 1: Two-route congestion network",
        TWO_ROUTE_NETWORK,
        NUM_DRIVERS,
    )

    run_strategy_comparison(
        "Experiment 2: Braess-style network with shortcut",
        BRAESS_NETWORK,
        NUM_DRIVERS,
    )

    compare_braess_shortcut(
        BRAESS_NETWORK_WITHOUT_SHORTCUT,
        BRAESS_NETWORK,
        NUM_DRIVERS,
    )

    run_adoption_experiment(
        "Experiment 3: Adoption rate experiment",
        TWO_ROUTE_NETWORK,
        NUM_DRIVERS,
    )


if __name__ == "__main__":
    main()

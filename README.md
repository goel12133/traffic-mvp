# Traffic Routing MVP

**Question:** Does giving every driver the individually optimal route always improve overall traffic flow?

My hypothesis is that there exists some adoption level where a routing system begins to *hurt* overall traffic, not because the routes are wrong, but because too many drivers receive identical recommendations and end up over-coordinating.



## The Problem Decomposition

Most routing systems (Google Maps, Waze) frame this as a shortest-path problem: find the fastest route for each driver individually. But that framing misses something important.

Every driver's decision changes the graph for everyone else. The moment a driver picks a route, the travel time on that route increases for anyone behind them. The problem is not "find the shortest path" but rather "distribute drivers across routes."

Two concepts from traffic theory shaped how I thought about this:

**Braess's Paradox** In certain networks, adding a new road makes overall travel times *worse*, because drivers rationally switch to the new route and cause more congestion than before. The individually rational decision is collectively irrational.

**Price of Anarchy** A measure of how much worse a system performs when everyone acts selfishly, compared to a central planner assigning routes optimally. A Price of Anarchy greater than 1 means selfish routing is costing everyone time.

These two ideas reframe the question as the goal is not to find the best route for each driver but rather it should be to find a distribution of drivers across routes that minimises total system travel time.



## Generic Traffic Model

Travel time on any road segment is modelled as:

```
time = T + k × n
```

Where:
- `T` = base travel time with no traffic
- `k` = congestion factor (how sensitive the road is to load)
- `n` = number of cars on that segment

This is intentionally simple. The goal at this stage is not realistic modelling but to test whether the effect can emerge at all under simplified conditions, before layering in more realistic assumptions.



## Orthogonality 

The road network is defined separately from the routing logic.

Networks are data structures (nodes, edges, congestion parameters). Routing strategies are functions that operate on any network. This separation means I can test Braess-style networks, partial-adoption experiments, and different congestion models without touching the routing algorithms etc.

```
network definition  ──►  routing strategy  ──►  result
     (data)               (function)           (metrics)
```

This also keeps the experiments honest as the same algorithm runs against all networks, so differences in output come from network structure, not implementation.



## Experiments

### Experiment 1: Two-route network

A simple network with two routes from A to D:

- **Short route** (A → B → D): low base time, high congestion sensitivity
- **Long route** (A → C → D): high base time, low congestion sensitivity

Four routing strategies are compared:

| Strategy | Description |
|---|---|
| Random | Each driver picks a route at random |
| Naive selfish | All drivers look at an empty network and pick the best-looking route |
| Sequential selfish | Each driver picks greedily based on current traffic |
| System-optimal | Each driver is assigned the route that minimises average travel time |

**Finding:** Sequential selfish routing can perform *worse* than random routing when the shorter route is congestion-sensitive. Drivers rationally pile onto the seemingly faster route, making it slower than the alternative they all ignored.

### Experiment 2: Braess's Paradox

A four-node network where a zero-cost shortcut connects the midpoints of two routes. Classical Braess setup.

**Finding:** Adding the shortcut increased average travel time under selfish routing. Every driver, acting rationally, takes said shortcut and this increased concentration of traffic makes everyone slower. Counterintuitively, this also implies that REMOVING a road would improve outcomes here.

The shortcut only helped when drivers were routed randomly. This is the paradox: a road that looks like an improvement destroys the implicit load-balancing that existed before.

### Experiment 3: Partial adoption

What happens as more drivers switch from random routing to the selfish app-based routing?

This tests the adoption-curve hypothesis wherein there may be a sweet spot where partial adoption improves flow, but full adoption tips into over-coordination and hurts it.



## Current Results

The simulation showed that routing behaviour can have a significant impact on overall traffic flow.

In the simple two-route network, naïve selfish routing performed much worse than both random routing and system-optimal routing because all drivers chose the same initially attractive route and created heavy congestion. However, sequential selfish routing performed nearly as well as the system-optimal solution.

The result most in line with the hypothesis came from the Braess-style network. Adding a shortcut increased the average travel time from 95.0 to 129.88, demonstrating Braess's Paradox: improving the network can sometimes make traffic worse when drivers respond selfishly to new routing options.

These results support the idea that traffic performance depends not only on road capacity, but also on how drivers are distributed across the network.


---

## Remaining questions / unknowns

The biggest unresolved question is how to model driver behaviour more realistically without losing the simplicity needed to isolate the effect. Specifically:

**Naive vs. predictive selfishness.** Right now, drivers react to current traffic. A more realistic driver might predict that everyone else is going to make the same choice leading him to route around the anticipated congestion. 

Other variables to explore later in rough order of interest:

- Different information quality across drivers (eg. waze vs gmaps vs no software)
- Dynamic traffic conditions (drivers entering at different times) not necessarily sequentially but also not silmantaneous
- Non-linear congestion models 
- Drivers with heterogeneous preferences, usually cost versus punctuality (distance vs time)



## Definition of Done (for this Tracer Bullet)

- [x] Demonstrate whether the over-coordination effect can emerge in a simplified environment
- [x] Produce reproducible results across multiple network configurations
- [x] Explain the mechanism (not just the outcome)
- [x] Build a framework extensible to more realistic assumptions

The framework is extensible: new networks are data, new strategies are functions, and neither needs to know about the other.



## Running the Simulation

```bash
python traffic.py
```

Requires Python 3.10+ (uses `itertools.pairwise`).

Output includes route counts, per-route travel times, average travel time, and Price of Anarchy for each experiment.

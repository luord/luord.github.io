from collections.abc import Collection
from functools import cmp_to_key
from typing import Protocol


class Environment[Individual, Genome](Protocol):
    def is_viable(self, subject: Individual) -> bool: ...

    def compare_fit(self, first: Individual, second: Individual) -> int: ...

    def find_mate(self, subject: Individual) -> Individual: ...

    def cross(self, fit: Individual, mate: Individual) -> Genome: ...

    def mutate(self, genome: Genome) -> Individual: ...


def find_fittest[Individual, G](
    population: Collection[Individual], environment: Environment[Individual, G]
) -> Individual:
    while (
        fit := max(population, key=cmp_to_key(environment.compare_fit))
    ) and not environment.is_viable(fit):
        mate = environment.find_mate(fit)

        brood = (environment.cross(fit, mate) for _ in range(len(population)))
        population = tuple(environment.mutate(gen) for gen in brood)

    return fit

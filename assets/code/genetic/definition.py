from collections.abc import Collection
from typing import Protocol


class Offspring[Individual](Protocol):
    def mutate(self) -> Individual: ...


class Population[Individual](Collection, Protocol):
    def select_random(self) -> Individual: ...

    def crossover(self, first: Individual, second: Individual)\
        -> Offspring[Individual]: ...

    def add(self, individual: Individual): ...

    def remove(self, individual: Individual): ...

    def find_mate(self, individual: Individual) -> Individual: ...


class Niche[Individual](Protocol):
    def tournament(self, pop: Collection[Individual])\
        -> tuple[Individual, Individual]: ...

    def can_thrive(self, individual: Individual) -> bool: ...


def algorithm[Individual](
    population: Population[Individual], niche: Niche[Individual]
) -> int:
    parent_a = population.select_random()
    parent_b = population.select_random()

    generations = 0

    while not niche.can_thrive(parent_a):
        base_offspring = population.crossover(parent_a, parent_b)
        real_offspring = base_offspring.mutate()
        population.add(real_offspring)

        fittest, unfit = niche.tournament(population)
        population.remove(unfit)
        parent_a, parent_b = fittest, population.find_mate(fittest)

        generations += 1

    return generations

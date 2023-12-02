from collections.abc import Collection
from typing import Protocol, TypeVar


class Individual(Collection, Protocol):
    ...


Ind = TypeVar('Ind', contravariant=True, bound=Individual)


class Offspring(Protocol):
    def mutate(self) -> Individual: ...


class Population(Collection, Protocol[Ind]):
    def select_random(self) -> Individual: ...

    def crossover(self, first: Ind, second: Ind) -> Offspring: ...

    def add(self, individual: Ind): ...

    def remove(self, individual: Ind): ...

    def find_mate(self, individual: Ind) -> Individual: ...


class Niche(Protocol[Ind]):
    def tournament(self, pop: Population) -> tuple[Individual, Individual]:
        ...

    def can_thrive(self, individual: Ind) -> bool: ...


def algorithm(population: Population, niche: Niche) -> int:
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

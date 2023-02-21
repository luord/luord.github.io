from collections.abc import Collection
from typing import Protocol, Self


class Individual(Collection, Protocol):
    @classmethod
    def generate_random(cls) -> Self:
        ...


class BasePopulation(Collection[Individual], Protocol):
    @classmethod
    def crossover(cls, a: Individual, b: Individual) -> Self:
        ...


class Population(Collection[Individual], Protocol):
    @classmethod
    def mutate_base(cls, base: BasePopulation) -> Self:
        ...

    @classmethod
    def find_mate(cls, individual: Individual) -> Individual:
        ...


class Niche(Protocol):
    def tournament_selection(self, population: Population) -> Individual:
        ...

    def can_thrive(self, individual: Individual) -> bool:
        ...


def algorithm(
    niche: Niche,
    Individual: type[Individual],
    BasePopulation: type[BasePopulation],
    Population: type[Population]
) -> int:
    parent_a = Individual.generate_random()
    parent_b = Individual.generate_random()

    generations = 0

    while not niche.can_thrive(parent_a):
        base_offspring = BasePopulation.crossover(parent_a, parent_b)
        offspring = Population.mutate_base(base_offspring)

        parent_a = niche.tournament_selection(offspring)
        parent_b = Population.find_mate(parent_a)

        generations += 1

    return generations

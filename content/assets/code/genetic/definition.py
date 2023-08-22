from collections.abc import Collection
from typing import Protocol, TypeVar


class Individual(Protocol):
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
        offspring = population.crossover(parent_a, parent_b)
        new_ind = offspring.mutate()
        population.add(new_ind)

        parent_a, worst = niche.tournament(population)
        population.remove(worst)
        parent_b = population.find_mate(parent_a)

        generations += 1

    return generations

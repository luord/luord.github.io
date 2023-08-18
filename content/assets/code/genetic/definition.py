from typing import Protocol, Self, TypeVar


class Individual(Protocol):
    @classmethod
    def generate_random(cls) -> Self:
        ...


I = TypeVar('I', bound=Individual, contravariant=True)


class BasePopulation(Protocol[I]):
    @classmethod
    def crossover(cls, a: I, b: I) -> Self:
        ...


class Population(Protocol[BasePopulation[I]]):
    @classmethod
    def mutate_base(cls, base: BasePopulation[I]) -> Self:
        ...

    @classmethod
    def find_mate(cls, individual: I) -> Individual:
        ...


P = TypeVar('P', bound=Population, contravariant=True)


class Niche(Protocol[P, I]):
    def tournament_selection(self, population: P) -> Individual:
        ...

    def can_thrive(self, individual: I) -> bool:
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

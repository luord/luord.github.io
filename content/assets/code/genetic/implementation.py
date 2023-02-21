from collections.abc import Iterable
from dataclasses import dataclass, field
from itertools import count
from random import Random
from string import ascii_lowercase
from typing import ClassVar, Self, cast

from definition import (
    algorithm,
    Individual as IIndividual,
    BasePopulation as IBasePopulation,
    Population as IPopulation
)


class Individual(tuple):
    LENGTH: ClassVar[int] = 50
    POOL: ClassVar[str] = ascii_lowercase
    _random: ClassVar[Random] = Random()

    @classmethod
    def generate_random(cls):
        base = cls._random.choices(cls.POOL, k=cls.LENGTH)

        return cls(base)


class BasePopulation(list[Individual]):
    SIZE: ClassVar[int] = 10
    _random: ClassVar[Random] = Random()

    @classmethod
    def crossover(cls, a: IIndividual, b: IIndividual) -> Self:
        offspring = cls()

        for _ in range(cls.SIZE):
            pair = [a, b]
            cls._random.shuffle(pair)
            first, second = pair
            division = cls._random.randint(1, Individual.LENGTH-1)
            offspring.append(Individual(
                f if ix < division else s
                for ix, (f, s) in enumerate(zip(first, second))
            ))

        return offspring


class Population(set[Individual]):
    MUTATION: ClassVar[int] = 900
    _random: ClassVar[Random] = Random()

    @classmethod
    def mutate_base(cls, base: IBasePopulation) -> Self:
        population = cls()

        for individual in base:
            mutated = next(
                ind for _ in count()
                if (ind := cls._mutate_individual(individual))
                not in population
            )
            population.add(mutated)

        return population

    @classmethod
    def find_mate(cls, individual: IIndividual) -> Individual:
        return cls._mutate_individual(individual)

    @classmethod
    def _mutate_individual(cls, individual: IIndividual) -> Individual:
        return Individual(
            cls._random.choices(
                (g, cls._random.choice(Individual.POOL)),
                weights=(cls.MUTATION, 1)
            )[0] for g in individual
        )


@dataclass
class Niche:
    THRESHOLD: ClassVar[int] = 45

    target: Individual = field(default_factory=Individual.generate_random)

    def tournament_selection(self, population: IPopulation) -> Individual:
        return cast(
            Individual,
            max(population, key=lambda ind: self._check_fit(ind))
        )

    def can_thrive(self, individual: IIndividual) -> bool:
        return self._check_fit(individual) >= self.THRESHOLD

    def _check_fit(self, individual: Iterable) -> int:
        return sum(a == b for a, b in zip(self.target, individual))


if __name__ == "__main__":
    print(algorithm(Niche(), Individual, BasePopulation, Population))

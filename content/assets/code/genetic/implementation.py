from collections.abc import Iterable
from dataclasses import dataclass, field
from itertools import count
from random import Random
from string import ascii_lowercase
from typing import ClassVar, Self, cast

from definition import algorithm


class Individual(tuple[str]):
    LENGTH: ClassVar[int] = 50
    POOL: ClassVar[str] = ascii_lowercase
    MUTATION: ClassVar[int] = 900
    _random: ClassVar[Random] = Random()

    @classmethod
    def generate_random(cls):
        base = cls._random.choices(cls.POOL, k=cls.LENGTH)

        return cls(base)

    def __and__(self, other: Self) -> Self:
        division = self._random.randint(1, self.LENGTH-1)
        return self.__class__(self[:division] + other[division:])

    def __pos__(self) -> Self:
        return self.__class__(
            self._random.choices(
                (gene, self._random.choice(self.POOL)),
                weights=(self.MUTATION, 1)
            )[0] for gene in self
        )


class BasePopulation(list):
    SIZE: ClassVar[int] = 10
    _random: ClassVar[Random] = Random()

    @classmethod
    def crossover(cls, a: Individual, b: Individual) -> Self:
        offspring = cls()

        for _ in range(cls.SIZE):
            pair = [a, b]
            cls._random.shuffle(pair)
            first, second = pair
            offspring.append(first & second)

        return offspring


class Population(set[Individual]):
    @classmethod
    def mutate_base(cls, base: BasePopulation) -> Self:
        population = cls()

        for individual in base:
            mutated = next(
                ind for _ in count()
                if (ind := +individual)
                not in population
            )
            population.add(mutated)

        return population

    @classmethod
    def find_mate(cls, individual: Individual) -> Individual:
        return +individual


@dataclass
class Niche:
    THRESHOLD: ClassVar[int] = 45

    target: Individual = field(default_factory=Individual.generate_random)

    def tournament_selection(self, population: Population) -> Individual:
        return cast(
            Individual,
            max(population, key=lambda ind: self._check_fit(ind))
        )

    def can_thrive(self, individual: Individual) -> bool:
        return self._check_fit(individual) >= self.THRESHOLD

    def _check_fit(self, individual: Iterable) -> int:
        return sum(a == b for a, b in zip(self.target, individual))


if __name__ == "__main__":
    print(algorithm(Niche(), Individual, BasePopulation, Population))

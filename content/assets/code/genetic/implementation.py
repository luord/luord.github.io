from collections.abc import Collection
from dataclasses import dataclass, field
from random import Random
from string import ascii_lowercase
from typing import ClassVar, Self

from definition import algorithm


class Individual(str):
    LENGTH: ClassVar[int] = 50
    POOL: ClassVar[str] = ascii_lowercase
    MUTATION: ClassVar[int] = 270
    _random: ClassVar[Random] = Random()

    def __new__(cls, base: str = ''):
        return super().__new__(
            cls,
            base or ''.join(cls._random.choices(cls.POOL, k=cls.LENGTH))
        )

    def __or__(self, other: Self) -> Self:
        division = self._random.randint(1, self.LENGTH-1)
        return self.__class__(self[:division] + other[division:])

    def __and__(self, other: Self) -> int:
        return sum(a == b for a, b in zip(self, other))


class Offspring(Individual):
    def mutate(self) -> Individual:
        return Individual(+self)

    def __pos__(self) -> str:
        return ''.join(self._random.choices(
            gene + self.POOL,
            weights=(self.MUTATION,) + (1,) * len(self.POOL)
        )[0] for gene in self)


class Population(set[Individual]):
    SIZE: ClassVar[int] = 10
    _random: ClassVar[Random] = Random()

    def __init__(self):
        return super().__init__(
            Individual() for _ in range(self.SIZE)
        )

    def select_random(self) -> Individual:
        return self._random.choice(list(self))

    def add(self, individual: Individual):
        return super().add(individual)

    def remove(self, individual: Individual):
        if len(self) <= self.SIZE:
            return

        return super().remove(individual)

    def crossover(self, first: Individual, second: Individual) -> Offspring:
        pair = [first, second]
        self._random.shuffle(pair)
        first, second = pair
        return Offspring(first | second)

    def find_mate(self, individual: Individual) -> Individual:
        return min(self, key=lambda ind: ind & individual)


@dataclass
class Niche:
    THRESHOLD: ClassVar[int] = 45

    target: Individual = field(default_factory=Individual)

    def tournament(
        self,
        pop: Collection[Individual]
    ) -> tuple[Individual, Individual]:
        return (
            max(pop, key=lambda ind: ind & self.target),
            min(pop, key=lambda ind: ind & self.target)
        )

    def can_thrive(self, individual: Individual) -> bool:
        return self.target & individual >= self.THRESHOLD


if __name__ == "__main__":
    print(algorithm(Population(), Niche()))

from dataclasses import dataclass, field
from itertools import chain, islice, repeat
from random import Random
from string import ascii_lowercase
from typing import Self

from definition import find_fittest


class Individual(str):
    LENGTH = 50
    POOL = frozenset(ascii_lowercase)
    MUTATION_RATE = 0.03

    _rng = Random()

    def __new__(cls, genome: str = '') -> Self:
        return super().__new__(cls, ''.join(
            cls._rng.choice(tuple(cls.POOL - {gene}))
            if not gene or cls._rng.random() < cls.MUTATION_RATE else gene
            for gene in islice(chain(genome, repeat("")), cls.LENGTH)
        ))

    def __or__(self, other: Self) -> int:
        return sum(s == o for s, o in zip(self, other))

    def __and__(self, mate: Self) -> str:
        return ''.join(
            self._rng.choice(s + m) for s, m in zip(self, mate)
        )


@dataclass
class Environment:
    THRESHOLD = 49

    target: Individual = field(default_factory=Individual)
    cycles: int = field(default=0, init=False)

    def is_viable(self, subject: Individual) -> bool:
        return (
            self._increment()
            or subject | self.target >= self.THRESHOLD
        )

    def compare_fit(self, first: Individual, second: Individual) -> int:
        return (
            (f := first | self.target) < (s := second | self.target) and -1
            or f > s
        )

    def find_mate(self, subject: Individual) -> Individual:
        return Individual(self.target & subject)

    def cross(self, fit: Individual, mate: Individual) -> str:
        return fit & mate

    def mutate(self, genome: str) -> Individual:
        return Individual(genome)

    def _increment(self):
        self.cycles += 1


if __name__ == "__main__":
    f = find_fittest({Individual() for _ in range(20)}, n := Environment())
    print(n, f)

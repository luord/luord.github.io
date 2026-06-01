#!/usr/bin/env -S uv run -s
# /// script
# dependencies = ["hypothesis", "pytest"]
# ///
import operator
from unittest.mock import patch

import pytest
from hypothesis import assume, given

from implementation import Individual, Environment, find_fittest


@given(...)
def test_tournament(
    unfit: Individual, population: set[Individual], env: Environment
):
    assume(not env.is_viable(unfit))
    assume(len(population) > 0)
    fit = find_fittest(population, env)

    assert env.compare_fit(fit, unfit) == 1


@pytest.mark.parametrize("mutation_rate, comparator", [
    (1, operator.ne), (0, operator.eq)
])
@given(env=..., base=...)
def test_mutate(env: Environment, base: Individual, mutation_rate, comparator):
    with patch.object(Individual, "MUTATION_RATE", new=mutation_rate):
        mutated = env.mutate(base)
        assert all(comparator(b, m) for b, m in zip(base, mutated))


@patch.object(Individual, "LENGTH", new=10)
@given(...)
def test_crossover(father: Individual, mother: Individual, env: Environment):
    offspring = env.cross(father, mother)

    assert set(offspring) <= set(father) | set(mother)


if __name__ == "__main__":
    import sys
    import subprocess

    subprocess.call([
        sys.executable,
        "-m",
        "pytest",
        "-W",
        "ignore::hypothesis.errors.SmallSearchSpaceWarning",
        __file__
    ])

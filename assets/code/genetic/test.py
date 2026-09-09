#!/usr/bin/env -S uv run -s
# /// script
# dependencies = ["hypothesis", "pytest"]
# ///
import operator
from unittest.mock import patch

import pytest
from hypothesis import assume, given, strategies as st

from implementation import Individual, Environment, find_fittest


st.register_type_strategy(Individual, st.text().map(Individual))


@given(...)
def test_tournament(
    unfit: Individual, population: set[Individual], env: Environment
):
    assume(not env.is_viable(unfit))
    assume(len(population) > 0)
    fit = find_fittest(population, env)

    assert env.compare_fit(fit, unfit) == 1


@pytest.mark.parametrize("do_mutate, matcher", [
    (1, operator.ne), (0, operator.eq)
])
@given(env=..., base=st.from_type(Individual).map(str))
def test_mutation(env: Environment, base: str, do_mutate, matcher):
    with patch.object(Individual, "MUTATION_RATE", new=do_mutate):
        mutated = env.mutate(base)

    assert matcher(base, mutated)


@patch.object(Individual, "LENGTH", new=10)
@given(...)
def test_crossover(f: Individual, m: Individual, env: Environment):
    offspring = env.cross(f, m)

    assert set(offspring) <= set(f) | set(m)


if __name__ == "__main__":
    import sys
    del sys.modules['hypothesis'], sys.modules['_hypothesis_globals']
    del assume, given, st
    pytest.main([__file__])

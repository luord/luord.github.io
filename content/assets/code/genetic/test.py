from hypothesis import given, strategies as st

from implementation import Individual, Niche, Population


st.register_type_strategy(Individual, st.builds(Individual, st.text(
    alphabet=Individual.POOL,
    min_size=Individual.LENGTH,
    max_size=Individual.LENGTH
)))


@given(...)
def test_crossover(parent_a: Individual, parent_b: Individual):
    offspring = Population().crossover(parent_a, parent_b)

    is_parent_a = is_parent_b = False

    for gene, a, b in zip(offspring, parent_a, parent_b):
        assert gene in (a, b)
        is_parent_a |= gene == a
        is_parent_b |= gene == b

    assert is_parent_a and is_parent_b


@given(...)
def test_tournament_selection(niche: Niche, population: Population):
    pop = set(population)
    winner, loser = niche.tournament(pop)

    while len(pop) > 1:
        assert winner in pop

        pop.remove(loser)
        _, loser = niche.tournament(pop)
    else:
        assert winner == loser

from hypothesis import given, strategies as st

from implementation import BasePopulation, Individual, Niche, Population


@given(
    st.data(),
    st.builds(Individual.generate_random),
    st.builds(Individual.generate_random)
)
def test_crossover(data, parent_a: Individual, parent_b: Individual):
    offspring = BasePopulation.crossover(parent_a, parent_b)

    individual = data.draw(st.sampled_from(offspring))

    shuffle = next(
        i == b for i, a, b in zip(individual, parent_a, parent_b)
        if a != b
    )

    first, second = (parent_b, parent_a) if shuffle else (parent_a, parent_b)

    split = next(
        ix for ix, a in enumerate(individual)
        if a != first[ix]
    )

    assert individual[:split] == first[:split]
    assert individual[split:] == second[split:]


@given(
    st.data(),
    st.builds(Niche),
    st.builds(
        Population,
        st.lists(st.builds(Individual.generate_random), min_size=1)
    )
)
def test_tournament_selection(data, niche: Niche, population: Population):
    winner = niche.tournament_selection(population)
    other_individual = data.draw(st.sampled_from(list(population)))

    assert winner in population
    assert niche._check_fit(winner) >= niche._check_fit(other_individual)

from hypothesis import given, strategies as st

from implementation import BasePopulation, Individual, Niche, Population

@given(st.data(), st.text(min_size=1), st.lists(st.text(min_size=1), min_size=1))
def test_tournament_selection(data, target: str, population: list[str]):
    target = Individual(target.split())
    population = Population(Individual(s.split()) for s in population)
    niche = Niche(target)

    winner = niche.tournament_selection(population)

    assert winner in population
    assert niche._check_fit(winner) >= niche._check_fit(data.draw(st.sampled_from(population)))

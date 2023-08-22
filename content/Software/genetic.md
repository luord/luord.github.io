title: A genetic algorithm implemented in Python
summary: An example of abstraction and analogy.
tags: software,algorithms,code,examples
date: 2023-03-01
status: published
image: assets/img/genetic/genes.jpg

Natural selection is, roughly, the likelihood of a given individual to survive long
enough to reproduce, and thus continue its species. Factor in mutations—random changes in the
genes—and the probability a given mutation has to help an individual survive (or not) in its
environment and the result is that some individuals are more likely to reproduce than others,
and thus more likely to pass on their mutations to the next generation, which will add
mutations of its own, ultimately causing the population to slowly change as these mutations
accumulate. Repeat this process over multiple generations across millions of years and we
get evolution.

Turns out that implementing these ideas, or at least analogies, in software can be useful to
solve certain problems, so let's write a simple program that exemplifies the process.

## Seed

There are multiple types of genetic algorithms with multiple different uses, but usually they
start with random data.

    :::python
    from typing import Protocol


    class Individual(Protocol):
      ...


    class Population(Protocol):
      def select_random(self) -> Individual: ...


    def algorithm(population: Population):
      parent_a = population.select_random()
      parent_b = population.select_random()

To keep things simple, we start with two parents that are selected randomly from the existing
population, and we'll go from there.[^protocols]

## Crossover

With our first pair in place, we can now produce the next "generation".

    :::python
    from collections.abc import Collection
    from typing import Protocol, TypeVar


    # ...
    Ind = TypeVar('Ind', contravariant=True, bound=Individual)


    class Offspring(Protocol):
      def mutate(self) -> Individual: ...


    class Population(Collection, Protocol[Ind]):
      # ...
      def crossover(self, first: Ind, second: Ind) -> Offspring: ...

      def add(self, new: Ind): ...


    def algorithm(population: Population):
      # ...

      offspring = population.crossover(parent_a, parent_b)
      new_ind = offspring.mutate()
      population.add(new_ind)

The crossover in genetic algorithms is the operation used to combine the genetic information of
two parents to produce offspring. But we can't just stop there, we need genetic variance to ensure
the population actually evolves over time. One form of variance is of course that the parents
are shuffled and a random number of genes is picked from each parent, but even that isn't enough as
it could leave us stuck[^pool].

Actual variance comes from the key element of **mutation**, the random chance that any given
offspring individual will have genes not present in the parents.[^offspring]

Finally, the new individual[^type] is, of course, a new member of the population so we add it.

## Natural Selection

At this point, we have parents and their offspring, what now? It's time to determine the goal.
Genetic algorithms are commonly used to find a good enough solution to certain types of,
often trial and error, problems that don't translate well to common normal algorithms.
Fortunately, the only thing resembling a "goal" in nature is simply thriving, surviving long
enough to reproduce, which can be interpreted as a long series of attempts and failures...
So let's do that, by introducing a "niche" and determining how well the individuals fit that niche.

    :::python
    # ...
    class Population(Collection, Protocol[Ind]):
      # ...
      def remove(self, individual: Ind): ...


    class Niche(Protocol):
      def tournament(self, pop: Population) -> tuple[Individual, Individual]:
        ...


    def algorithm(population: Population, niche: Niche):
      # ...
      fittest, worst = niche.tournament(population)
      population.remove(worst)

Nature is ruthless, and so is our algorithm. In nature, only the fittest perpetuate their
genes, and in our algorithm, only that individual that best fits the niche is the
one to continue. This is usually called "tournament selection" in genetic algorithm parlance.

Finally, to maintain our analogy (and really to prevent our population from growing without bound)
we remove the least fit individual from the population.

## Generations

We have almost completed the algorithm, but the mere fact that we've found an individual that fits
the niche better than others doesn't mean we've actually found one that _occupies_ the niche, the
likelihood of achieving that in just the first generation is nil. We'll need many generations, so we need
to repeat the process until we find such individual.

    :::python
    # ...
    class Population(Collection, Protocol[Ind]):
      # ...
      def find_mate(self, individual: Ind) -> Individual: ...


    class Niche(Protocol[Ind]):
      # ...
      def can_thrive(self, individual: Ind) -> bool: ...


    def algorithm(population: Population, niche: Niche) -> int:
      parent_a = population.select_random()
      parent_b = population.select_random()

      generations = 0

      while not niche.can_thrive(parent_a):
        offspring = population.crossover(parent_a, parent_b)
        new_ind = offspring.mutate()
        population.add(new_ind)

        fittest, worst = niche.tournament(population)
        population.remove(worst)
        parent_a, parent_b = fittest, population.find_mate(fittest)

        generations += 1

      return generations

There are several options here, one commonly used in real genetic algorithms is to pick the two
fittest instead of just one and make those "reproduce", producing an entirely new population
and keep iterating from there. But to keep our
natural analogy going, let's instead assume that our fittest finds instead a "suitable mate"[^mate] in another
member of the population, which also adds another source of variance.

Ultimately, the point here is iteration: continually doing the crossover and tournament selection until we meet
our goal.

---

And there we have it, that `algorithm` function represents our full genetic algorithm, in a way I hope is self-explanatory
enough. That function _should_ work without change as long as it receives arguments that actually implement
the [protocols][] properly.

[Here's a file][definition] with the complete definition, and [here's a file][implementation] with a
string-based implementation of the algorithm, along with the function being run.

Now, before finishing, you'll notice that I talked very little about the actual _problems_ that could
be solved with this type of algorithm... Well that's true, because the point of this post was the
algorithm itself. That said, I might write a follow up with a practical example.

## Appendix (On implementation and testing)

I mentioned above that implementation doesn't matter and it indeed doesn't but for the sake
of completeness—to fully explain the genetic algorithm—I wanted to go over what happens during
crossover and tournament selection. However, we can write [tests][] to do that instead
of explaining the implementations line by line![^jokes]

    :::python
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

This is our test for crossover: As you can see, first it finds whether the parents were shuffled
around, then confirms that all the genes up to a split point come from the parent that was positioned
first, and that all the genes from that split point on come from the second. In short, it confirms
that the offspring is indeed the combination of the parents' "genes".

    :::python
    # ...
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

Tournament selection is even simpler: Confirm that our winner in the population does actually beat
(or at worst ties) with any other individual in the population according to the rules of the niche.

[^protocols]: I use protocols because Python's structural subtyping[protocols][] is pretty good at
properly representing a [domain][]. In simpler terms: we only care about what our objects can _do_.
Indeed, the code I'll be showing shouldn't throw errors in [mypy][] or [pyright][].
[^collection]: And this is why our `Population` implements the `Collection` protocol; for all intents
and purposes of the algorithm, a population is a collection of individuals.
[^pool]: If we stick to just the parents' genomes, then the target will never be reached if it requires a
gene that neither of the parents has.
[^offspring]: The intermediate class `Offspring` fulfills two purposes here: to explicitly show
the mutation step (instead of leaving it as an implementation detail of crossover) and to rely
on the type system. We'll know we have a real individual only if it was selected from an
existing population or if it's the result of mutation from the crossover of two parents.
[^type]: On that note, you might have noticed that an "Individual" is represented only by an empty
protocol and a generic type (and the type variable might not even be needed after Python 3.12 drops).
This is on purpose; the algorithm doesn't need to care what an individual _is_.
[^mate]: _How_ it finds it is an implementation detail, hopefully one that excludes its parents.
[^jokes]: Since, as we all know, "code is for what, tests are for why, and comments are for jokes".

[domain]: {filename}/Engineering/domain.md
[mypy]: https://mypy-lang.org/
[pyright]: https://github.com/microsoft/pyright
[protocols]: https://peps.python.org/pep-0544/
[definition]: {static}/assets/code/genetic/definition.py
[implementation]: {static}/assets/code/genetic/implementation.py
[tests]: {static}/assets/code/genetic/test.py

title: A genetic algorithm implemented in Python
summary: An example of abstraction and analogy.
tags: software,algorithms,code,examples
date: 2023-03-01
status: published
image: assets/img/genetic/genes.jpg

Natural selection is, roughly, the likelihood of a given individual to survive long
enough to reproduce, and thus continue its species. Factor in mutations—random changes in the
genes—and the probability a given mutation has to help an individual survive (or not) in its
environment and the result is that some individuals are more likely to reproduce than others.
Those fitter individuals are more likely to pass on their mutations to the next generation, which will add
mutations of its own, ultimately causing the population to slowly change as these mutations
accumulate. Repeat this process over multiple generations across millions of years and we
get evolution.

Turns out that implementing these ideas, or at least analogies, in software can be useful to
solve certain problems, so let's write a simple program that exemplifies the process.

## Seed

There are multiple types of genetic algorithms with multiple different uses, but usually they
start with a data sample.

    :::python
    from collections.abc import Collection
    from typing import Protocol


    class Population[Individual](Collection, Protocol):
      def select_random(self) -> Individual: ...


    def algorithm[Individual](population: Population[Individual]):
      parent_a = population.select_random()
      parent_b = population.select_random()

To keep things simple, we start with two parents that are selected randomly from the existing
population, and we'll go from there.[^protocols]

## Crossover

With our first pair in place, we can now produce the next "generation".

    :::python
    class Offspring[Individual](Protocol):
      def mutate(self) -> Individual: ...


    class Population[Individual](Collection, Protocol):
      # ...
      def crossover(self, first: Individual, second: Individual)\
          -> Offspring[Individual]: ...

      def add(self, individual: Individual): ...


    def algorithm[Individual](population: Population[Individual]):
      # ...
      base_offspring = population.crossover(parent_a, parent_b)
      real_offspring = base_offspring.mutate()
      population.add(real_offspring)

The ***crossover*** in genetic algorithms is the operation used to combine the data of
the parents to produce offspring. But we can't just stop there, we need genetic variance to ensure
the population actually evolves over time. One form of variance is of course that the parents
contribute different characteristics selected at random from each parent, but even that isn't enough as
it could leave us stuck[^pool].

Actual variance comes from the key element of **mutation**, the random chance that any given
offspring individual will have genes not present in the parents.[^offspring]

Finally, the new individual is, of course, a new member of the population so we add it[^type].

## Natural Selection

At this point, we have parents and their offspring, what now? It's time to determine the goal.
Genetic algorithms are commonly used to find a good enough solution to certain types of,
often trial and error, problems that don't translate well to common normal algorithms.
Fortunately, the only thing resembling a "goal" in nature is simply thriving, surviving long
enough to reproduce...
So let's do that, by introducing a "niche" and determining how well the individuals fit that niche.

    :::python
    # ...
    class Population[Individual](Collection, Protocol):
      # ...
      def remove(self, individual: Individual): ...


    class Niche[Individual](Protocol):
      def tournament(self, pop: Collection[Individual])\
        -> tuple[Individual, Individual]: ...


    def algorithm[Individual](
      population: Population[Individual], niche: Niche[Individual]
    ):
      # ...
      fittest, unfit = niche.tournament(population)
      population.remove(unfit)

Nature is ruthless, and so is our algorithm. In nature, only the fittest perpetuate their
genes, and in our algorithm, only that individual in a group[^collection] that best fits the niche is the
one to continue. This is usually called "***tournament selection***" in genetic algorithm jargon.

Finally, to maintain our analogy (and really to prevent our population from growing without bound)
we remove the least fit individual from the population.

## Generations

We have almost completed the algorithm, but the mere fact that we've found an individual that fits
the niche better than others doesn't mean we've actually found one that _thrives_ in the niche; the
likelihood of achieving that in just the first generation is nil. We'll need many generations, so we need
to repeat the process until we find such individual.

    :::python
    # ...
    class Population[Individual](Collection, Protocol):
      # ...
      def find_mate(self, individual: Individual) -> Individual: ...


    class Niche[Individual](Protocol):
      # ...
      def can_thrive(self, individual: Individual) -> bool: ...


    def algorithm[Individual](
      population: Population[Individual], niche: Niche[Individual]
    ) -> int:
      parent_a = population.select_random()
      parent_b = population.select_random()

      generations = 0

      while not niche.can_thrive(parent_a):
        base_offspring = population.crossover(parent_a, parent_b)
        real_offspring = base_offspring.mutate()
        population.add(real_offspring)

        fittest, unfit = niche.tournament(population)
        population.remove(unfit)
        parent_a, parent_b = fittest, population.find_mate(fittest)

        generations += 1

      return generations

There are several options here, one commonly used in real genetic algorithms is to pick the two
fittest instead of just one and make those "reproduce", producing an entirely new population
and continue iterating from there. But to keep our
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

    from implementation import Individual


    st.register_type_strategy(Individual, st.builds(Individual, st.text(
      alphabet=Individual.POOL,
      min_size=Individual.LENGTH,
      max_size=Individual.LENGTH
    )))

Before anything is done, we have to tell [hypothesis][] how to create an `Individual` that
actually fits our implementation. Only then we move onto the tests:

    :::python
    # ...
    from implementation import Population

    @given(...)
    def test_crossover(parent_a: Individual, parent_b: Individual):
      offspring = Population().crossover(parent_a, parent_b)

      is_parent_a = is_parent_b = False

      for gene, a, b in zip(offspring, parent_a, parent_b):
        assert gene in (a, b)
        is_parent_a |= gene == a
        is_parent_b |= gene == b

      assert is_parent_a and is_parent_b

This test tells us everything we need to know about what
happens in `crossover` without actually having to check the implementation: We don't care how it's
done, but we do care that every gene in the offspring comes from one of the parents, and that _both_
parents had an input.

    :::python
    # ...
    from implementation import Niche


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

Tournament selection is a bit trickier to test because the calculation for each fittest _is_ an
implementation detail, but one the whole idea depends upon. We could simply repeat the implementation
here and assert that the winner and loser were calculated correctly but then the test would no
longer work if we changed the metric (or changed what an individual is entirely).

In these cases, we have to step back and think of invariants: what is always true about the tournament
selection? As long as the winner remains in the population and no other individuals are added, it will _always_ be the winner. And that's what we test: We systematically remove each loser until only one
individual is left in the population; that individual _must_ still be the original winner!

[^protocols]: I use protocols because Python's [structural subtyping][protocols] is pretty good at
properly representing a [domain][]. In simpler terms: we only care about what our objects can _do_.
On that note, the code I'll be showing shouldn't throw errors in [mypy][] or [pyright][].
[^pool]: If we stick to just the parents' genomes, then the target will never be reached if it requires a
gene that neither of the parents has.
[^offspring]: The intermediate class `Offspring` fulfills two purposes here: to explicitly show
the mutation step (instead of leaving it as an implementation detail of crossover) and to rely
on the type system. We'll know we have a real individual only if it was selected from an
existing population or if it's the result of mutation from the crossover of two parents.
[^type]: You might have noticed that an "Individual" is represented only by generic type arguments.
This is on purpose: the algorithm doesn't need to care what an individual _is_.
[^collection]: You might have noticed that in the type annotation, I used `Collection` instead of `Population`
(which is itself a collection). That's because the tournament could be done over any group of individuals, it
doesn't have to be a population specifically, and we gotta be "liberal in what we accept".
[^mate]: _How_ it finds it is an implementation detail, hopefully one that excludes its parents.
[^jokes]: Since, as we all know, "code is for what, tests are for why, and comments are for jokes".

[protocols]: https://typing.readthedocs.io/en/latest/spec/protocol.html#protocols
[domain]: {filename}/Engineering/domain.md
[mypy]: https://mypy-lang.org/
[pyright]: https://github.com/microsoft/pyright
[hypothesis]: https://hypothesis.readthedocs.io/en/latest/
[definition]: {static}/assets/code/genetic/definition.py
[implementation]: {static}/assets/code/genetic/implementation.py
[tests]: {static}/assets/code/genetic/test.py

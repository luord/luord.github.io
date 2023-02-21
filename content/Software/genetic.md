title: A genetic algorithm implemented in Python
summary: There are way too many type hints in this code.
tags: software,algorithms,code,examples
date: 2023-02-05
status: draft
image: /assets/img/splash/domain.jpg

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
    from collections.abc import Collection
    from typing import Protocol, Self


    def algorithm(Individual: type[Individual]):
      parent_a = Individual.generate_random()
      parent_b = Individual.generate_random()


    class Individual(Collection, Protocol):
      @classmethod
      def generate_random(self) -> Self:
        ...

This is our first step, to keep things simple we start with two parents that represent
our random seed and we'll go from there.

You might have noticed that `Individual` is a `Protocol`, which include no implementation.
This is on purpose, as [we don't actually care][domain] about the implementation in
order to understand the algorithm. [Protocols][] and Python's structural subtyping
allow themselves quite well to showcase this[^mypy].

## Crossover

Alright, we have our first pair, which means we can now produce the next "generation".

    :::python
    # ...
    def algorithm(
      Individual: type[Individual],
      BasePopulation: type[BasePopulation],
      Population: type[Population]
    ):
      # ...

      base_offspring = BasePopulation.crossover(parent_a, parent_b)
      offspring = Population.mutate_base(base_offspring)


    class BasePopulation(Collection[Individual], Protocol):
      @classmethod
      def crossover(cls, a: Individual, b: Individual) -> Self:
        ...


    class Population(Collection[Individual], Protocol):
      @classmethod
      def mutate(self, base: BasePopulation) -> Self:
        ...

The crossover in genetic algorithms is the operation used to combine the genetic information of
two parents to produce offspring[^collection]. But we can't just stop there, we need genetic variance to ensure
the population actually evolves over time. One form of variance is of course that random genes
are picked from each parent for producing the given offspring, but even that isn't enough as
it could leave us stuck[^pool].

Actual variance comes from the key element of **mutation**, the random chance that any given
offspring individual will have genes not present in the parents.

## Natural Selection

At this point, we have parents and their offspring, what now? It's time to determine the goal.
Genetic algorithms are commonly used to find a good enough solution to certain types of,
often trial and error, problems that don't translate well to common normal algorithms.
Fortunately, the only thing resembling a "goal" in nature is simply thriving, surviving long
enough to reproduce, which can be interpreted as a long series of attempts and failures...
So let's do that, by introducing a "niche" and determining how well the individuals fit that niche.

    :::python
    # ...

    def algorithm(
      niche: Niche,
      Individual: type[Individual],
      BasePopulation: type[BasePopulation],
      Population: type[Population]
    ):
      # ...
      fittest = niche.tournament_selection(offspring)

    # ...
    class Niche(Protocol):
      def tournament_selection(self, population: Population) -> Individual:
        ...

Nature is ruthless, and so is our algorithm. In nature, only the fittest perpetuate their
genes, and in our algorithm, only that offspring individual that best fits the niche is the
one to continue. This is usually called "tournament selection".

## Generations

We have almost completed the algorithm, but the mere fact that we've found an individual that fits
the niche better than others doesn't mean we've actually found one that _occupies_ the niche, the
likelihood of achieving that in just the first generation is nil. We'll need many generations, so we need to repeat
the process.

    :::python
    # ...

    def algorithm(
      niche: Niche,
      Individual: type[Individual],
      BasePopulation: type[BasePopulation],
      Population: type[Population]
    ):
      parent_a = Individual.generate_random()
      parent_b = Individual.generate_random()

      generations = 0

      while not niche.can_thrive(parent_a):
        base_offspring = BasePopulation.crossover(parent_a, parent_b)
        offspring = Population.mutate_base(base_offspring)

        parent_a = niche.tournament_selection(offspring)
        parent_b = Population.find_mate(parent_a)

        generations += 1

      return generations
      
    # ...
    class Population(Collection[Individual], Protocol):
      # ...

      @classmethod
      def find_mate(cls, individual: Individual) -> Individual:
        ...


    class Niche(Protocol):
      # ...

      def can_thrive(self, individual: Individual) -> bool:
        ...

There are several options here, one commonly used in real genetic algorithms is to pick the two
fittest instead of just one and make those the parents of the next generation. But to keep our
natural analogy going, let's instead assume that our fittest finds instead a "suitable mate" from
another population, which also gives us another source of genetic variance.

---

And there we have it, that `algorithm` function represents our full genetic algorithm, in a way I hope is self-explanatory
enough. That function _should_ work without change as long as it receives arguments that actually implement
the protocols properly.

[Here's a file][definition] with the complete definition, and [here's a file][implementation] with a
string-based implementation of the algorithm, alogn with the function being run.

## Appendix (On Implementation)

I mentioned above that implementation doesn't matter and it indeed doesn't but for the sake
of completeness I wanted to bring notice to the implementation of the `crossover` and
`tournament_selection` methods.

    :::python
    # ...
    class BasePopulation(list[Individual]):
      SIZE: ClassVar[int] = 10
      _random: ClassVar[Random] = Random()

      @classmethod
      def crossover(cls, a: IIndividual, b: IIndividual) -> Self:
        offspring = cls()

        for _ in range(cls.SIZE):
          pair = [a, b]
          cls._random.shuffle(pair)
          first, second = pair
          division = cls._random.randint(1, Individual.LENGTH-1)
          offspring.append(Individual(
            f if ix < division else s
            for ix, (f, s) in enumerate(zip(first, second))
          ))

        return offspring

I like to think it's pretty self-explanatory: One approach to doing crossover is taking the
first random number of "genes" from the first parent and the remaining genes from the second.
The parents are shuffled too so that their order doesn't actually matter.

    :::python
    # ...
    @dataclass
    class Niche:
      THRESHOLD: ClassVar[int] = 45

      target: Individual = field(default_factory=Individual.generate_random)

      def tournament_selection(self, population: IPopulation) -> Individual:
        return cast(
          Individual,
          max(population, key=lambda ind: self._check_fit(ind))
        )

      def _check_fit(self, individual: Iterable) -> int:
        return sum(a == b for a, b in zip(self.target, individual))

Tournament selection is even simpler: Compares each individual against something. For real genetic algorithms,
this something is usually done by measuring how well each given solution actually works.

[^mypy]: You'll notice that the code in every step of this article won't throw [mypy][] errors or
[pyright][] errors.
[^collection]: And this is why our `Individual` implements the `Collection` protocol; for all intents
and purposes of the algorithm, an individual is a collection of "genes".
[^pool]: If we stick to just the parents' genomes, then the target will never be reached if it has a gene
that neither of the parents does.

[domain]: {filename}/Engineering/domain.md
[mypy]: https://mypy-lang.org/
[pyright]: https://github.com/microsoft/pyright
[Protocols]: https://peps.python.org/pep-0544/
[definition]: {static}/assets/code/genetic/definition.py
[implementation]: {static}/assets/code/genetic/implementation.py

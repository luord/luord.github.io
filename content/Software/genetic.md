title: A genetic algorithm implemented in Python
summary: There are way too many type hints in this code.
tags: software,algorithms,code,examples
date: 2022-11-23
status: draft
image: /assets/img/splash/domain.jpg

Natural selection is, roughly, the likelihood of a given individual to survive long
enough to reproduce, and thus continue its species. Factor in mutations—random changes in the
genes—and the probability a given mutation has to help an individual survive (or not) in its
environment and the result is that some individuals are more likely to reproduce than others, and thus more likely
to pass on their mutations to the next generation, that will add mutations of its own,
ultimately causing the population to slowly change as these mutations accumulate.
Repeat this process over multiple generations across millions of years and we get evolution.

Turns out that implementing these ideas, or at least analogies, in software can be useful to
solve certain problems, so let's write a simple program that exemplifies the process.

## Random Number Nature

Let's get the hardest part out of the way first as it will be necessary through most of
the algorithm.

    from typing import Protocol

    class Split(bool): ...

    class Order(bool): ...

    class Mutagenic(list[str]): ...

    class Selector(Protocol):
        def get_genome_split(self) -> Split: ...

	def get_split_order(self) -> Order: ...

	def get_mutagenic(self) -> Mutagenic: ...

`Selector` represents the randomness of nature, like for example
which genes a parent passes to its offspring, which genes a child takes from each parent,
or what mutations are likely to occur. Of course, in real life there are millions of
other factors, but as it pertains to this example, those are the random factors we need.[^protocol]

## Individual in its environment

    :::python
    class Environment(str): ...


    class Individual(str):
        def __new__(cls, value: str, env: Environment):
	    if len(value) != len(env):
                raise ValueError("Incompatible environment for individual")

	    return super().__new__(cls, value)

    	def get_survival_rate(self, env: Environment) -> int:
	    return sum(i == e for i, e in zip(self, env))

	def get_genome_section(self, split: Split) -> str:
	    return self[split::2]


Alright, that's a good "start", we have an environment class and an individual class,
and the latter can calculate its survival likelihood in the former[^under].
`Individual` can also return a requested section of its "genome" according to the
random `Split` we saw earlier.

## Populations and best adapted individuals

    :::python
    class AptPair(NamedTuple):
        f: Individual
	m: Individual

	def merge(self, split: Split, order: Order) -> Individual:
	    f = self.f.get_genome_section(split)
	    m = self.m.get_genome_section(not split)

	    offspring = ""
	    for a, b in zip(f, m):
	        offspring += a + b if order else b + a

	    return Individual(offspring)

    class Population(list[Individual]):
        def get_successsful_pair(self, env: Environment) -> AptPair:
	    f = Population(self[::2])
	    m = Population(self[1::2])

	    return AptPair(f.get_best_adapted(env), m.get_best_adapted(env))

	def get_best_adapted(self, env: Environment) -> Individual:
	    return max(self, key=lambda ind: ind.get_survival_rate(env))

Now we have a population that can determine which of its belonging
individuals are the most successful. This is done via tournament selection, which is to
say that the population is split in a given number of sections and the individual
with the best survival rate of each section is picked for the next step. For the sake
of brevity, I did just two subdivisions, which give us a pair apt to "reproduce".

## Crossover

    :::python
    def crossover(pair: AptPair, split: Split, order: Order, mutagenic: Mutagenic) -> Individual:
        f = AptPair.f.get_genome_half(split.f)
	m = AptPair.m.get_genome_half(split.m)

	offspring = Individual(f + m if order else m + f)
	offspring.mutate(

This is the core of the algorithm, really, "Selector" stands in for the randomness of nature,
it determines which section of the genetic code of the parents will be selected and how they will
merge to form the offspring, which is what happens in the `merge` function.
Finally, `Selector` also determines what mutations will the offspring have.

## ... Over

    :::python
    def mutate(ind: Individual, mutagenic


[^protocol]: Isn't it beautiful how we can discuss this without caring about the underlying
implementation? `Selector` is just a protocol pending implementation, as we don't yet need it working and
can talk about it [without having or needing to know how it works][domain].
[^under]: Love that the fact of these being strings is incidental, we can literally change that without
renaming the classes for a different implementation and it wouldn't impact the algorithm.
Same thing applies to the `Split` or `Mutagenic` classes returned by `Selector`.


[domain]: {filename}/Engineering/domain.md
        def get_genome_half(self, split: Split, order: Order) -> str:
	    return self[split::2]

        def mutate(self, mutagenic: Mutagenic, env: Environment) -> None:
	    mutated = ""
	    for mutant, current in zip(mutagenic, self):
	        mutated += mutant or current

	    self = Individual(mutated, env)

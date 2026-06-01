title: A genetic algorithm implemented in Python
summary: An example of abstraction and analogy.
tags: software,algorithms,code,examples
date: 2023-03-01
status: published
image: assets/img/genetic/genes.jpg

Natural selection is, roughly, the likelihood of a given individual to survive long
enough to reproduce, and thus continue its species. Factor in mutations (random changes in the
genes) and the probability a given mutation has to help an individual survive (or not) in its
environment, and the result is that some individuals are more likely to reproduce than others.
Those fitter individuals will pass on their mutations to the next generation, which will add
mutations of its own, ultimately causing the population to slowly change as these mutations
accumulate. Repeat this process over multiple generations across millions of years and we
get evolution.

Turns out that implementing these ideas, or at least analogies, in software can be useful to
solve certain problems, so let's write a simple program that exemplifies the process.

## Population and Environment

The basis of ecology is populations and environments; how individuals interact with each other
and their environment, and the feedback loop that emerges as the environment responds.

    :::python
    from collections.abc import Collection
    from typing import Protocol


    class Environment(Protocol):
        ...


    def find_fittest(population: Collection, environment: Environment): ...

There are multiple types of genetic algorithms, commonly used to find good enough
solutions to certain types of, often trial and error, problems that don't translate
well to more traditional algorithms. What they tend to have in common is starting with
a data sample and a set of patterns in the data we want to reach by the end, roughly represented
here by the population and the environment[^protocols], respectively.

## Natural Selection

Evolution is what we want to represent; the survive and adapt process is the only
real "goal" in nature. Here's where Darwin's truth comes into play: Some individuals
are more likely to reproduce than others; the fitter the individual,
the more likely it is to pass on its genes.

    :::python
    from functools import cmp_to_key
    # ...
    class Environment[Individual](Protocol):
        def compare_fit(self, first: Individual, second: Individual) -> int:
            ...

        def find_mate(self, subject: Individual) -> Individual: ...


    def find_fittest[Individual](
        population: Collection[Individual],
        environment: Environment[Individual]
    ):
        fit = max(population, key=cmp_to_key(environment.compare_fit))
        _ = environment.find_mate(fit)

Nature is ruthless, and so is our algorithm. In nature, only the fittest perpetuate their
genes, and in our algorithm, only the individual[^type] in a given generation that best fits the niche is the
one to continue. This is usually called "***tournament selection***" in genetic algorithm parlance.
The typical approach is to select a given number of fit individuals for the next step, but
to maintain our ecological analogy, we go with two: the fittest individual and a suitable mate
found in the environment[^mate].

## Crossing

We have the fittest individual, the one most likely to reproduce, and a suitable mate. For evolution
to happen, they need to do just that: produce new generations when the environment is right.

    :::python hl_lines="12"
    # ...
    class Environment[Individual, Genome](Protocol):
        # ...
        def cross(self, fit: Individual, mate: Individual) -> Genome: ...


    def find_fittest[Individual, G](
        # ...
        environment: Environment[Individual, G]
    ):
        # ...
        mate = environment.find_mate(fit)

        _ = (environment.cross(fit, mate) for _ in range(len(population)))

The ***crossover*** in genetic algorithms is the operation used to combine the data of
the parents to produce some offspring (as many as in the original population in our case, to make
things easier). But for now it's just the basic data, the "genetic material"; not a true
individual, because the most important step for evolution (and genetic algorithms) comes next.

## Mutation

As the "X-Men" movie put it well, the key of evolution is mutation. It's not enough to just
combine the genes of the parents, random changes in the data need to happen for the population to change
over time.

    :::python hl_lines='6'
    # class Environment...
        def mutate(self, genome: Genome) -> Individual: ...


    # def find_fittest...
        brood = (environment.cross(fit, mate) for _ in range(len(population)))
        population = tuple(environment.mutate(gen) for gen in brood)

In real life, the environment doesn't often cause mutations unless things went really, really,
_radioactively_ wrong, so in here we're using `environment` as stand-in for "it happens in nature"
because indeed, mutations happen spontaneously. Anyhow, if things go well, these new
individuals should be mostly mixes of the parents, each with some small changes to its combined genome[^genome].
This group is now our next population, to continue our search for the fittest.

## Generations

We have almost everything in place, the only thing missing is... well, to keep on. Evolution takes
many generations; it goes on forever. In our case, until we find the fittest possible individual
in the given environment.

    :::python hl_lines="8 13"
    # class Environment...
        def is_viable(self, subject: Individual) -> bool: ...
        # ...


    def find_fittest[Individual, G](
        # ...
    ) -> Individual:
        while (
            fit := max(population, key=cmp_to_key(environment.compare_fit))
        ) and not environment.is_viable(fit):
            # ...
        return fit

The first step of the algorithm was selection, and it still is, but now we also add a loop
that checks whether the current fittest in the population is, well, fit enough, and to continue
iterating until it is. By extension, if the current fittest isn't "viable",
nobody else in the population is. Once we find a viable subject, we return it; after all, in
a real application, we'd need to reach the goal for a reason, meaning we might have to
use that optimal data for something else.

---

And there we have it, that `find_fittest` function represents our full genetic algorithm, in a way I hope is self-explanatory
enough. That function _should_ work without change as long as it receives arguments that actually implement
the [protocols][] properly.

[Here's a file][definition] with the complete definition, and [here's a file][implementation] with a
string-based implementation of the algorithm, along with the function being run.

Now, before finishing, you'll notice that I talked very little about the actual _problems_ that could
be solved with this type of algorithm... Well that's true, because the point of this post was the
algorithm itself.

## Appendix (On implementation and testing)

I mentioned above that implementation doesn't matter and it indeed doesn't but for the sake
of completeness, to fully explain the genetic algorithm, I wanted to go over what happens during
tournament selection, mutation and crossover. But we don't need to pour over implementation details;
we can write [tests][] to understand instead![^jokes]

Tournament selection is a bit tricky to test, because we are mostly using python primitives.
It's pointless to test `max`.

But what we can test is
invariants, what doesn't change regarding the selection, what is always true? We actually
already mentioned a useful invariant before: If the fittest individual in a population isn't
fit enough, then nobody else in the population can be. Or, to put it another way, an individual
we already know is the fittest possible, will always be a better fit than one we know it's not.

    :::python
    #!/usr/bin/env -S uv run -s
    # /// script
    # dependencies = ["hypothesis", "pytest"]
    # ///
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

Using property based testing with [hypothesis][], we confirm the invariant: Test only for
unfit individuals, find the fittest for the environment in a non-empty population, then check that
such fittest is indeed always better than the initial unfit.

Next is mutation. Now, it's hard to think of an invariant for mutation: a mutation may happen or
it may not. Luckily, in my code, how often a mutation happens is a configuration detail,
and we can tune it without having to care how it's used in the actual implementation[^config].

    :::python
    import operator
    from unittest.mock import patch

    import pytest
    # ...

    @pytest.mark.parametrize("mutation_rate, comparator", [
        (1, operator.ne), (0, operator.eq)
    ])
    @given(env=..., base=...)
    def test_mutate(env: Environment, base: Individual, mutation_rate, comparator):
        with patch.object(Individual, "MUTATION_RATE", new=mutation_rate):
            mutated = env.mutate(base)
            assert all(comparator(b, m) for b, m in zip(base, mutated))

Updating the mutation rate, we create two invariants: When the rate is 100%, mutation is total;
the mutated individual cannot share genes with the base genome. If the rate is 0%, mutation
can't happen; the individual's genes must be identical to the base genome.

Finally, crossover. This one has a simple invariant: All the offspring genes must come from
one of the two parents, so we test just that:

    :::python
    @patch.object(Individual, "LENGTH", new=10)
    @given(...)
    def test_crossover(father: Individual, mother: Individual, env: Environment):
        offspring = env.cross(father, mother)

        assert set(offspring) <= set(father) | set(mother)

Simple enough, each single gene in an offspring must come from the union of all the genes of the
parents. I made another configuration change: Since by default the length of the string is 50
and only lowercase characters, the odds are that every individual will have them all, making this
test trivial. Reducing it to 10 makes it possible for the parents to have at least some
different "genes". Then the test is meaningful.

[^protocols]: I use protocols because Python's [structural subtyping][protocols] is pretty good at
properly representing a [domain][]. In simpler terms: we only care about what our objects can _do_.
On that note, the code I'll be showing, at every step, shouldn't throw errors in either type checkers like
[ty][], [mypy][] or [pyright][], nor linters like [flake8][] or [ruff][].
[^type]: You might have noticed that "Individual" is represented only by generic
type arguments. This is on purpose: the algorithm doesn't need to care what an individual
_is_ and should work on any data type.
[^mate]: _How_ it finds it is an implementation detail, hopefully one that excludes the rest of the
population (hence why the population isn't a parameter), as they're intended to be related.
It'll become clear later.
[^genome]: The generic type `Genome` fulfills two purposes here: to explicitly show
the mutation step (instead of leaving it as an implementation detail of crossover) and to rely
on the type system: We'll know we have a real individual only if it was selected from an
existing population or environment, or if it's the result of mutation from the crossover of two parents.
[^jokes]: Since, as we all know, "code is for what, tests are for why, and comments are for jokes".
Not to mention that I made every single method body a one liner because I wanted to push the limits
of how "[cleverly][]" I could write it.
[^config]: Now, whether configuration is implementation or not, a lot has been written about. I think
if they are properly separated, then no, configuration is independent and used _by_ the implementation.

[protocols]: https://typing.readthedocs.io/en/latest/spec/protocol.html
[domain]: {filename}/Engineering/domain.md
[ty]: https://docs.astral.sh/ty/
[mypy]: https://mypy-lang.org/
[pyright]: https://microsoft.github.io/pyright/
[flake8]: https://flake8.pycqa.org/en/latest/
[ruff]: https://docs.astral.sh/ruff/
[hypothesis]: https://hypothesis.readthedocs.io/en/latest/
[definition]: {static}/assets/code/genetic/definition.py
[implementation]: {static}/assets/code/genetic/implementation.py
[tests]: {static}/assets/code/genetic/test.py
[cleverly]: {filename}/Engineering/refactoring.md

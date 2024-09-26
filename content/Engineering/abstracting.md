title: Practical refactoring: Abstractions
tags: software,development,craftsmanship,engineering
summary: Improving code by way of writing specific and self-describing abstractions.
date: 2022-03-31
image: /assets/img/abstracting/idea.jpg
status: published

In [my last post][refactoring]{.u-in-reply-to}, we did a basic rundown of a very convoluted short algorithm to make
more explicit what was actually happening in it. That by itself goes a long way in improving how readable the code is, and thus makes it easier to maintain.
I've seen small improvements like that be welcome enthusiastically among different teams, but we can go
further.

I remember a project I worked on where there was basically no separation of concerns between request
handling boilerplate, database connection boilerplate and actual business logic; everything was handled
within the same functions. It was a nightmare. I was hired to create some new APIs, but it took me just a
week of trying to create new handlers like that to decide that such was no way to live. I took it
upon myself to refactor that code. It bears reasserting that when refactoring, it's good—and often enough—to first reach for the lowest hanging fruit and in that code the easiest improvement was, of course,
separating code that dealt with different things into different functions, and calling those new functions from the old ones.

Now, the small script we're going through does really only one thing, but that doesn't mean we can't
divide some responsibilities by way of abstracting away some code **not** directly related to that
one thing. If we do this, we improve the code in at least three ways:

1. The algorithm itself becomes more immediately obvious; it's easier to understand what the code does.
2. By abstracting the supporting/boilerplate code, we make it possible to reuse those same structures
somewhere else.
3. This gives us a opportunity to bring the code in step with the domain: using names specific to what
we're doing instead of talking exclusively about basic data types.

## The abstractions

Something I didn't mention in my last post is that the small method we're refactoring is actually part of a basic
genetic algorith I implemented for fun. Well, genetic algorithms deal with populations, so what if
instead dealing with "lists" of "strings", we create an actual `Population` class/data type that does
what we need our populations to do:

    :::python
    class Population(list):
        def __iter__(self) -> Iterable[Self]:
            return iter(self[x::2] for x in range(2))

Not complicated, now we know that a population is a list, but one that when iterated just produces
two sublists: the two halves of the original. We _can_ improve it further, but this is enough for
what we need[^premature].

We have our population, but our genetic algorithm is not of random things; it specifically looks for
individuals that match a given root individual, with the purpose of each generation to be closer to that individual.

Let's give it a try:

    :::python
    class Individual(str):
        def __and__(self, other: Self):
            return sum(ch_s == ch_o for ch_s, ch_o in zip(self, other))

For our "model"[^genetic] we know that we need a specific type of string that when compared with another will
return the number of identical characters. So we do just that: create a `str` subclass that
can "intersect" with other strings of the same type, and give a numeric value representing how well
they match.

With these two abstractions alone, our method improves considerably:

    :::python
    def get_best_matches(self) -> WinnerPair:
        # self.population: Population[Individual]
        # self.root: Individual
        winners = WinnerPair()
        for half in self.population:
            winner = max(half, key=lambda ind: ind & self.root)
            winners.append(winner)
        return winners

I _like_ it. We get each member of the winner pair from half of the population, and notice how the code
doesn't show things we don't need to know to understand the steps:

1. How do we get each half of the population? That doesn't matter for understanding the algorithm; we just
need to know that we're getting a half. How that half is gathered is up to the implementtion in `Population`
which we can check if we need to, or we could change it if we have to: Like instead of appending the
odd-positioned items to a half and the even-positioned to the other half, we could just literally split it
at the central index.
2. To get the winner we're comparing how well is the intersection between each individual and the root
(`self.root`, renamed from `self.word`[^word], in this case). How is that intersection calculated/found?
That's entirely an implementation detail, which again we can check and/or change in `Individual`
if we have to. We could even make individuals a different type instead of strings, make a comparison
appropriate for that type, and we wouldn't need to change **anything** in this method.

Notice that, at the end of my previous post, I said that we could use abstractions instead of relying
on comments to tell us what the data types are supposed to represent. There are still comments in this
piece of code... but that comment is just to note _what_ abstractions we're using, and is there just
for description purposes. In the full code it would be completely redundant, since the types of
`self.population` and `self.root` would already be defined somewhere else. Likely at the top of the class
this method belongs to.

Nonetheless, we could still make those comments explicit in the code[^jokes] by way of, say, making them
arguments to the method. However, _that_ would no longer be a refactoring[^zero]... But we can cheat a little
bit:

    :::python
    def get_winners(
      population: Population[Individual], root: Individual
    ) -> WinnerPair:
        winners = WinnerPair()
        for half in population:
            winner = max(half, key=lambda ind: ind & root)
            winners.append(winner)
        return winners

    def get_best_matches(self) -> WinnerPair:
        return get_winners(self.population, self.root)

Basically, we create a new _function_ that isn't necessarily tied to a class (note the lack of `self`) and we
call that function from our method. This gives us the potential advantage of reusing that very same winner finding
logic somewhere else if the opportunity arises.

## Hindsight

So there you have it, we improved the code, considerably, just by moving a few lines around and making
what we're doing and using more explicit. It goes without saying that this would help us communicate between the developers _and_ with
the product team (if any) much more easily.

Ideally, in a good codebase, discussing the code and discussing the
business model would entail very similar expressions, as the code would just be a literal (with caveats of course) representation
of that business model. Hopefully this post showed how such a thing could be achieved.

This is a subject I really, really like and I'm hoping to keep writing about it.

[^premature]: When refactoring, it's easy to get lost making increasingly minute improvements. We always
gotta remember that premature optimization is the root of all evil and that abstractions can easily
become unnecessary indirections. This is a fine line, and sometimes I don't spot it, so it's important to
remember that the goal is to make the code _more_ maintainable instead of perfect from the get go (which is impossible anyway). In an
actual product, it also helps to remember what I think as the rule zero of Software Engineering:
"fight for the users". If something we're doing won't improve the users'
experience in any meaningful way, it might be best left alone.
[^genetic]: This genetic algorithm in particular just iterates over populations that increasingly
resemble the root word.
[^word]: In my opinion, the naming of the root individual as `self.word` was a code smell born out of
the usage of basic data types instead of proper abstractions. It was a way to hint at the developer that
the comparison was between strings. Using proper types/classes, we no longer need to do that.
[^jokes]: After all, "code is for what, tests are for why and comments are for jokes" (which is also a
joke... or is it?)
[^zero]: If "improve the easiest thing first" is rule one of refactoring, then "do ***not***, under any
circumstance, change the contract" is rule zero of refactoring. To put it another way: if we have a good
test suite, a proper refactoring shouldn't change the result of _any_ test. Anything other than that is
an actual change in the behavior of the application/system, and it better have been agreed upon.



[refactoring]: {filename}/Engineering/refactoring.md

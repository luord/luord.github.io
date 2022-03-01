title: Practical refactoring: 'clever' code
tags: software,development,craftsmanship
summary: Practical example of the problems with clever code and the benefits of refactoring.
date: 2022-02-28
status: published
image: /assets/img/refactoring/clever.jpg

Look at this code

    :::python
    def get_best_matches(self) -> WinnerPair:
        """
        Divide population in half.
        Pick the word closest to the matching word in each half.
        """
        return WinnerPair(*map(
            lambda population_half: max(
                population_half,
                default="",
                key=lambda word: sum(
                    a == b for a, b in zip(word, self.word)
                )
            ),
            (self.population[::2], self.population[1::2])
        ))

I'm not gonna deny it, I liked writing it, I like that it is technically a single function call[^class],
the usage of lambdas and the built-in Python functions used for handling, well, functions and iterables.
What can I say? It makes me feel "clever" because technically it's code that requires certain level of
familiarity with the language.

It's also a total mess. I literally spent an entire afternoon explaining this "short" piece of code
to an experienced engineer who had already invested a few months getting familiar with Python.

This code is me at my most self-indulgent and I'm well aware I would never have written this outside
of a [prototype meant only for me to play around][proto]. Code like this is **not** meant to live in a
system worked at by more than one developer. It'd be a nightmare to maintain, as only the one who wrote
it could possibly understand it. Hell, I wrote this and I had to struggle a bit puzzling what it actually
did.

In short, this code is ripe for improvement, which is exactly what I'm gonna do.

# Unclear iterations

The first thing that jumps at me upon seeing this code is that there are three nested iterations in it,
but it's very difficult to tell which one is which or where each one ends.
An easy first fix is then relying less on built-in functions and making the iterations more explicit
via `for` statements.

    :::python
    def get_best_matches(self) -> WinnerPair:
        # Get the words closest to the target in each half of the population
        winners = WinnerPair()
        for population in (self.population[x::2] for x in range(2)):
            scores = []
            for word in population:
                similarity = 0
                for char_word, char_target in zip(word, self.word):
                    similarity += chard_word == char_target
                scores.append((word, score))
            winner = max(scores, key=lambda score: score[1])
            winners.append(winner[0])
        return winners

Looks quite different, doesn't it? It would seem to someone completely unfamiliar with Python that
I changed more than replacing the function calls with `for`s, but that's truly _all_ I did:

1. The first function was `map` which is doing _something_ to both halves of the population.
2. The second function was `max` which is picking the highest according to _something_ in each word in
the population.
3. The third function was `sum` which is actually calculating that previous "something": In this case,
how similar is the current word with the target word.

I then reused `max`, but it's now clearer what maximum value of what it's being picked. I will not lie:
I hesitated with leaving the `sum` as it was as I felt that with the other replacements it was clear enough,
but then I saw the opportunity to further clarify that we were comparing the current word with the target word.
On the other hand, I did leave `zip` as it was, as that one **is** clear enough to me.[^craft]

---

Aside: Someone with some familiarity with algorithm analysis might see three nested `for` loops and
pale at the "cubic" complexity, but this function isn't iterating over the population input
(let's call it "n") multiple times. It's instead iterating only once over the _total characters_ input
(let's say "m"). In short: This iteration only visits each character in the population once.

The word list (but not each word) _is_ visited twice because of the `max` function, but since two is a
constant, it remains of linear complexity.

---

Anyhow, those "straightfoward" changes are enough to at least being able to tell what the function
is doing line by line, but it can be better.

As it is, we're doing a bunch of operations over basic data types with a comment explaining what
those data types are supposed to represent. We could instead explicitly define our own abstractions over
those data types and let those abstractions tell us what they can or can't do, or how they should be
used.

But I feel like that is interesting enough for its own post, so see you in the next part!

[^class]: Well, a function call wrapped in a class instantiation, but who's nitpicking?
[^craft]: I firmly think that Software Engineering **is** engineering, and I have no problem calling myself "engineer" over, say, "craftsman", but there _is_ a subjective factor to some decisions.

[proto]: https://gitlab.com/luord/prototype

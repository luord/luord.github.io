title: Type variance
status: published
date: 2023-08-22 18:45

I spent a while fixing up the [genetic][] algorithm I wrote a while ago; up
until the version that is up now, I didn't really like how it looked and the reason was
the type hints. It simply didn't click to me why the classes from the implementation
weren't compatible with the protocols in the definition and why I had to create the
type variables (which I find really ugly, and hopefully won't be required anymore in the near
future). Reading up on how to improve it led me to the concept
of variance, of which I only had a vague memory from college.

Writing this note to ensure it doesn't become a vague memory again:

- If something cannot be replaced whatsoever, either by subclass or superclass, it's deemed
_invariant_ in its context. An example is a location: A city cannot be replaced
by one of its streets, nor can a region be treated as if it were one of its cities.
- If something can be replaced by a subclass, it's deemed _covariant_ in its context.
An example is authorization: If you need a prescription for a regular painkiller, any
licensed physician can give it to you, even if the physician happens to be a cardiologist or
a pediatrician; but you can't get it from someone who isn't certified to do so.
- If something can be replaced by a superclass, it's deemed _contravariant_ in its context.
An example is capacity: If you can run, it follows that you can do something that only
needs for you to walk, or for you to be able to move from place A to B at all. The opposite
doesn't follow: just because you can walk doesn't mean you'll be able to run a
marathon.

[genetic]: {filename}/Software/genetic.md

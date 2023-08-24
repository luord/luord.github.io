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
_invariant_ in its context. An example is identity: A city cannot be replaced
by one of its streets, nor it can be treated as its whole surrounding region.
- If something can be replaced by a subclass, it's deemed _covariant_ in its context.
An example is possession: If you need something with a camera, then any standalone camera,
smartphone or tablet will do. A telescope, however, might not.
- If something can be replaced by a superclass, it's deemed _contravariant_ in its context.
An example is action: If you can run, it follows that you can do something that only
needs for you to walk. Conversely, just because I see you walking I can't assume you can run
a marathon.

[genetic]: {filename}/Software/genetic.md

*[identity]: Being
*[possession]: Having
*[action]: Doing

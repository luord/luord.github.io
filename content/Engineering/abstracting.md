status: draft

# Abstracting

Instead of doing operations directly over basic data types with a comment explaining what those data
types are supposed to be, we could explicitly define our own abstractions and let those abstractions
tell us what they can or can't do.

Let's start with `Population`:

    :::python
    class Population(list):
        def __iter__(self):
            return iter(self[x::2] for x in range(2))

Not complicated, what 

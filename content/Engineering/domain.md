title: Domains of engineers and users
summary: Improving communication by writing code that describes the domain more closely.
tags: software,development,engineering,refactoring
date: 2022-04-30
status: published
image: /assets/img/splash/domain.jpg

I finished [my last post][abstracting] by mentioning how refactoring can help us achieve a code base where discussing
the code and discussing the domain model can be analogous or even entail similar discussions. That's
a topic that deserves a deeper looking into.

## Experts on different domains

Imagine this conversation:

> End user/Product owner: "We'd like for the URL of the Foo to have the provided identifier instead of these random characters."

> Engineer: "Oh, by default the framework adds a UUID as the primary key, which is also used for URLs; we'll update it."

> End user/Product owner: "Is that a front-end change or a back-end change?"

Now, now, that's an exaggeration as I've worked with plenty of users and product people who were well
versed enough on technical details—often because they *had* to pick up the terminology—to understand what the developer was talking about
in that exchange, but I hope this gets the idea across: Too often, there's a gap in shared terminology that hinders the communication between
engineers and users.

And here's an example in the other direction:

> End user/Product owner: "We need the aggregated results of the 'Foo' to be calculated from the monthly 'bar' instead of the weekly 'bar' from now on."

> Engineer: "Understood, I'll add it to the backlog and change it as soon as possible."

> Engineer (later, to another engineer or the tech lead): "Where the hell do the aggregated results value come from? Is that in the database? How is it called there? And what even is `bar`?"

Now that one is no exaggeration; I've had that exact conversation over the years, multiple times.
And I've been on both sides of that last question too. Of course, I've also been in projects where there was enough rapport between
the engineering and product teams for the engineer to simply ask the product owner right away... But the problem still persists,
only in the form of periodic repetitive conversations instead of the latency caused by the developer looking for someone who understands.

The point is that engineers are experts on the domain of software engineering, while users
are experts on *their* own domain, which they're hoping it gets easier to do with the
application/platform/system they bought/subscribed to, or hired the engineers to create/maintain.

## Code and stories

Let's imagine that the user/product owner comes at us with the following requirement:

> As a user, I want to store my "Foo" with the "jon", "doe",
"bar" and "baz" values. With the understanding that "baz" is seven times
"bar".

After the appropriate back and forth, we come to the following [user story][stories]:

Store Foo
: Create a new model in `cool_framework` used to store the periodic `Foo` of the
user. The fields are `jon` (unique string), `doe` (integer, 100 by default),
and `bar` (float, cannot be empty); `baz` will be dynamically generated from `bar`.
A UUID field will be included as primary key by the framework.

This user story is of course lacking a way for users to actually submit the data they want to store[^form],
but it already has more than enough to show how the mismatch in communication starts: The user/product owner
could very well ask "what the hell is a UUID?"[^float]

I should point out that I am in no way condemning this approach. It's perfectly fine and how around ninety
percent of the projects I've worked on have looked.

But now let's look at the code that fulfills the user story:

    :::python
    from cool_framework import models


    class Foo(models.Model):
      jon = models.StringField(unique=True)
      doe = models.IntegerField(default=100)
      bar = models.FloatField(nullable=False)

      @models.computed_property
      def baz(self):
        return self.bar * 7

Again, this is perfectly fine; I currently work in projects whose code looks like this (with a
billion more fields and methods, of course), and there aren't problems, usually.

The thing is while this code can trivially be discused among engineers, it can't be discussed
by or with users. By this point, both groups are essentially speaking different languages: The users
talk about whatever Foo is, how the "jon" group performed this week, when the "baz" could change, etc.;
the engineers, conversely, are talking about fields, properties, tables, migrations, etc.

And this works! Most of my experience has had this kind of separation and the teams work and the product
is delivered. But what if the language gap could be narrowed?

## A shared language

Let's rephrase that story:

Store Foo
: Create a class/type/struct[^class] `Foo` where the user can store multiple instances of the following
values: `jon` (type `ProvidedIdentifier`), `doe` (type `UserEstimation`), and `bar` (type `PeriodicResults`);
`baz` (type `AggregatedResults`) is calculated from `bar`.

I just made up those types, but what's important here is that we're to assume that those types *mean something* to
the users. Whatever is in "jon", the users usually call it the "provided identifier" of whatever Foo is; they know
that "bar" is the "periodic results" of whatever it is that the users do. Ditto for the other fields.

With that understanding, let's rewrite the code to start illustrating why representing the domain more explicitly is important:

    :::python
    from decimal import Decimal


    class ProvidedIdentifier(string):
      class Meta:
        unique = True

    class UserEstimation(int):
      class Meta:
        default = 100

    class PeriodicResults(Decimal):
      class Meta:
        nullable = False

    class AggregatedResults(Decimal):
      FACTOR: int = 7

      def __new__(self, pr: PeriodicResults):
        return super().__new__(self, pr * self.FACTOR)


    class Foo:
      jon: ProvidedIdentifier
      doe: UserEstimation
      bar: PeriodicResults

      @property
      def baz(self) -> AggregatedResults:
        return AggregatedResults(self.bar)

Is the code more verbose? In total, absolutely[^lesscode] but it too became clearer
about the *what* we're dealing with: We can assume that the signatures of those classes came from discussions with the users,
where they described what that data means in their business and how it's supposed to behave.
Sure, `doe` is still a string, `bar` a floating point value, etcetera, but now the developers can talk about
the code in terms similar to what the users talk about, which also means they'll talk to the *users* in those terms too.

Let's reimage the conversations from the start, but now with the assumption that all the code is like this:

Well, for starters the first conversation no longer makes sense as another win from these changes is that we decoupled
our business logic from whatever framework we're using[^clean]... As long as the framework treats the business code as source of truth anyway.

As for the second,

> End user/Product owner: "We need the aggregated results of the 'Foo' to be calculated from the monthly 'bar' instead of the weekly 'bar' from now on."

> Engineer: "Just to make sure, `baz` is the aggregated results and `bar` is the periodic results, correct?"

> End user/Product owner: "Correct!"

> Engineer: "Cool, I'll get it done."

Let's be real, it's likely that the engineer still doesn't know what the hell these "results" are or why the users care about them, but now at least it might be easier
to pinpoint what needs to change without having to find someone who might be more familiar with the domain.

Finally, it bears mentioning that this approach doesn't solve all communication problems: The engineers will never be domain experts on the users' domain, so there will
always be questions, specially when creating new features as the developers will need to ask what the new classes/types will need for fields and metadata[^terminology];
as for the users/product owners, the decoupling with the framework and the increasing reliance on native language constructs means that the number of technical details they need
to have an idea about becomes smaller, but not zero.

Regardless, giving the team (both involved users and developers) a way to more fluidly discuss the product is a huge step forward in my book.

## A caveat

All of that is pretty nice; however, the boilerplate the users don't care about still needs to exist *somewhere*. Maybe abstracted and hidden away in specific modules or even
internal libraries that have their own repos, but finding and correcting leaky abstractions is a neverending battle, so those
discussions that ideally should be among engineers only might find their way in conversations with the users.

Imagine a world where we didn't need to abstract the boilerplate for every project; that it simply didn't exist.
In that ideal world, we could just drop some native classes/structs/etc that contain all the business logic and *only* the business logic to some tool(s),
and the tool would automagically take care of all the wiring needed for the application to reach the end user.

I've given a lot of thought to such an idea, and maybe it's a pipe dream, but stranger things happen in this industry all the time.

[^form]: Let's say a form in some web site/application.
[^float]: Or, for that matter "what are strings and floats?" You never know!
[^class]: Or whatever construct your favorite language uses to group data, if any!
[^lesscode]: But hey, the code of the `Foo` class itself got simpler.
[^clean]: Yay for clean architecture!
[^terminology]: In other words, some conversations for the developers to make the business rules clearer, which they then can express in the code!

[abstracting]: {filename}/Engineering/abstracting.md
[stories]: {filename}/Engineering/stories.md

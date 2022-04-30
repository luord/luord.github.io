title: Domains of engineers and users
tags: software,development,engineering,refactoring
date: 2022-04-30
status: published
image: /assets/img/splash/domain.jpg

I finished [my last post][abstracting] by mentioning how refactoring can help us achieve a code base where discussing
the code and discussing the domain model can be analogous or even entail similar discussions. That's
a topic that deserves a deeper looking into.

# Experts on different domains

Imagine this conversation:

> End user/Product owner: "We'd like for the URL of the Foo to have the provided identifier instead of these random characters."
> Engineer: "Oh, by default we add a UUID as the primary key and the framework uses the PK for URLs, we'll update it."
> End user/Product owner: "Is that a front-end change or a back-end change?"

Now, now, that's an exaggeration as I've worked with plenty of users and product people who were well
versed enough on technical details—often because they *had* to pick up the terminology—to understand what the developer was talking about
in that exchange. And usually the developer would say something more like "oh yeah, the update started
hiding them, I'll get it fixed right away" when talking with less or non technical people. But I hope this
gets the idea across: Too often, there's a gap in knowledge that hinders the communication between
engineers and users.

And it can totally happen in the other direction:

> End user/Product owner: "We need the 'baz' value of the 'Foo' to be calculated from the monthly 'bar' instead of the weekly 'bar' from now on."
> Engineer: "Understood, I'll get it added to the backlog and change it as soon as possible."
> Engineer (later, to another engineer or the tech lead): "Where the hell does the `bar` value come from? Is that in the database? How is it called there? And what even is `baz`?"

Now that one is no exaggeration; I've had that exact conversation over the years, multiple times.
And I've been on both sides of that last question too.

The point is that engineers are experts on the domain of software engineering, while users
are experts on *their* own domain, which they're hoping it gets easier to do with the
application/platform/system they bought/subscribed to, or hired the engineers to create/maintain.

# Code and stories

Let's imagine that the user/product owner comes at us with the following requirement:

> As a user, I want to store my "Foo" with the "jon", "doe",
"bar" and "baz" values. With the understanding that "baz" is seven times
"bar".

After the appropriate back and forth, we come to the following [user story][stories]:

Store Foo
: Create a new model in `cool_framework` used to store the periodic `Foo` of the
user. The fields are `jon` (unique string), `doe` (integer, 100 by default),
and `bar` (float, cannot be empty); `baz` will be dynamically generated from `bar`.
A UUID field will be included as primary key.

This user story is of course lacking a way for users to actually submit the data they want to store[^form],
but it already has more than enough to show how the mismatch in communication starts: The user/product owner
could very well ask "what the hell is a UUID?"[^float]

I should point out that I am in no way condemning this approach. It's perfectly fine and how around ninety
percent of the projects I've worked on have looked.

But now let's look at the code that fulfills the user story:

    :::python
    from cool_framework import models


    class Foo(models.Model):
      id = models.UUIDField(primary=True)
      jon = models.StringField(unique=True)
      doe = models.IntegerField(default=100)
      bar = models.FloatField(nullable=False)

      @models.computed_property
      def baz(self):
        return self.bar * 7

Again, this is perfectly fine; I currently work in projects whose code looks like this (with a
billion more fields and methods, of course), and there aren't problems, usually.

The thing is, while this code can trivially be discused among engineers; it can't be discussed
by or with users. By this point, both groups are essentially speaking different languages: The users
talk a out whatever Foo is, how the "jon" group performed this week, how the "baz" could change, etc.;
the engineers, conversely, are talking about fields, properties, tables, migrations, etc.

And this works! Most of my experience has had this kind of separation and the teams work and the product
is delivered. But what if the language gap could be narrowed?

# A shared language

Let's rephrase that story:

Store Foo
: Create a class/type/struct[^class] `Foo` where the user can store multiple instances of the following
values: `jon` (type `ProvidedIdentifier`), `doe` (type `UserEstimation`), and `bar` (type `PeriodicResults`);
`baz` (type `AggregatedResults`) is calculated from `bar`.

I just made up those types, but what's important here is that we're to assume that those types *mean something* to
the users. Whatever is in "jon", the users usually call it the "provided identifier" of whatever Foo is; they know
that "bar" is the "periodic results" of whatever it is that the users do. Ditto for the other fields.

Let's "refactor" the code to start illustrating why that's important:

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

Quite a few things changed here and the code is more verbose, but it is also both more explicit of the *what* we are dealing with:
We can assume that the signature of those classes came from discussions with the users, `doe` is still a string, `bar` a floating
point value, etcetera, but now the developers can talk about them in terms similar to what the users talk about.

Let's reimage the conversations from the start, but now with the assumption that all the code is like this:

Well, for starters the first conversation no longer makes sense as another win from these changes is that we decoupled
our business logic from whatever framework we're using.[^clean]

As for the second,

> End user/Product owner: "We need the 'baz' value of the 'Foo' to be calculated from the monthly 'bar' instead of the weekly 'bar' from now on."
> Engineer: "Just to make sure, `baz` is the aggregated results and `bar` is the periodic results, correct?"
> End user/Product owner: "Correct!"
> Engineer: "Cool, I'll get it done."

Of course, the engineer most likely still doesn't know what the hell these "results" are or what the users use them for, but now at least it might be easier
to pinpoint what needs to change without having to discuss it with someone else who might be more familiar with the domain.

Of course, this approach doesn't solve all communication problems: The engineers will never be domain experts on the users' domain, so there will
always be questions, specially when creating new features as the developers will need to ask what the new classes/types will need for fields and metadata;
as for the users/product owners, the decoupling with the framework and the increasing reliance on native language constructs means that the number of technical details they need
to have a "vague" idea about becomes smaller.

Regardless, giving the team (both involved users and developers) the tools to more fluidly discuss the product is a huge plus in my book.

That said, however, the boilerplate still needs to exist *somewhere*, but at least this shows that it can be abstracted and hidden away as much as possible and any problems
that come from whatever frameworks/databases/etc we use can be discussed by the developers without having first to become familiar with *all* the terminology specific to the project.[^tool]

[^form]: Let's say a form in some web site/application.
[^float]: Or, for that matter "what are strings and floats?" You never know!
[^class]: Or whatever construct your favorite language uses to group data, if any!
[^clean]: Yay for clean architecture!
[^tool]: Now imagine if we didn't need to abstract the boilerplate for every project; that it simply didn't exist.
In that ideal world, we could just drop some native classes/structs/etc that contain all the business logic and *only* the business logic to some tool(s),
and the tool would automagically take care of all the wiring needed for the application to reach the end user.

[abstracting]: {filename}/Engineering/abstracting.md
[stories]: {filename}/Engineering/stories.md

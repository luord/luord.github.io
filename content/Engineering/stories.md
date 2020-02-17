title: Creating stories from requirements
tags: architecture,design,model,musings,craftsmanship
summary: On crafting actionable development stories from requirements
date: 2020-02-01
status: published
image: /assets/img/splash/stories.jpg

A few weeks ago, one of my best friends came to me with an idea for an application. Unlike most (if not all) of my ideas, this one I actually believe to have potential so I asked him to prepare a list of requirements we could use to at least have a rough goal to aim for with this application. He delivered, and I was presented a good enough list... And I did nothing with it, I've been letting it sit there, all unfulfilled potential. But that changes now!

I've been working as a software engineer for a while and that experience, the [manifesto][], what I remember from my college studies and what I've read regarding system design all point to the same conclusion: Having a fixed list of tasks and dedicating too much time to it is pointless because requirements change like waves in the sea.

However, I still feel it's important to have a set of stories to work on, both to have a general idea of what the system is and how it's supposed to work, as well as for documenting progress; nothing kills motivation like the feeling you're not actually advancing towards your goal. Besides, we control the requirements in this case and, even though waves are fickle, [the global conveyor belt][belt] is still a thing. Much like with that overly elaborate metaphor, my goal is not to describe how every single detail in the application is supposed to work, but more a general description of each functionality, and general details on how to implement it.

With that in mind, I'll show how I approached turning that requirements list written in the "as a user" format into stories that developers can actually work on. I'll forgo things like "story points" or "acceptance criteria" because not only are those restrictive, I'm doing this as a developer for developers—all two of us—and what I care about is what to do and how to do it. And that's also the reason I won't be using stuff like certain project management tool that most software development teams are familiar with whose name I won't mention, at the risk of summoning giant lizards.[^jira]

In fact, this is a good point to mention [sourcehut][], Drew DeVault's cool set of tools for creating software that's very reminiscent of how the biggest open source projects are maintained. I'm going to be creating these stories using sourcehut's todo, which is to say: simple issues.

Without further ado, let's take one of the requirements as example, one that is universal enough that I can use without risking IP: user accounts. This is an abbreviation of my friend's requirement:

> As a user I can create an account in the application, with an email or using social networks (an email should be sent introducing the platform upon registration).

As mentioned, my goal with the stories is knowing what to do and how to do it, from a developer's perspective. Part by part, this is the architecture[^arch] that this requirement defines:

1. The application has a domain, and this domain includes the entity User because that's what we want to create.
2. The application has some sort of data layer that the application interfaces with to store this User data.
3. The application has adapters that _interface_ with third parties to retrieve the user data, social networks in this case.
4. The application has the **use case** "create user" that is called in two different ways: using email or using the adapters mentioned above.
5. The application has an _interface_ that the user employs to send the email and other data, or to trigger the retrieval from third parties.
6. The application has a second **use case**, which is to send an automated email to the, well, email provided by the user upon successful creation.

With that rough outline, we have an idea for two or three stories, because at this stage is better to restrict stories to the number of use cases, or to the number of times all use cases are instantiated across the application.[^cases] Of course, stories ultimately can involve *editing* use cases too; the point is that we should make the stories about the application business rules whenever possible.

The stories mentioned here are deliberately vague on the tech stack because I want this to be applicable for as many developers as possible.

Create User from email
: Create an Use Case that accepts raw data as well as a data repository[^postgres] and creates an instance of the User domain model using the raw data. It then passes this data to the repository for creation.

: Create an interface adapter[^flask] that receives data (including email) submitted by an user and passes it to the aforementioned Use Case, alongside the database repository.

: Create a view[^web] that allows the user to submit this data to the adapter.[^server]

Create User from third party
: Create an interface adapter that gathers data (including email) about an user sent from third parties[^dance]. It passes this data to the create user Use Case alongside the database repository.[^clean]

: Create a view that allows the user to go through the third party communication cycle.

Send email on user creation
: Edit Create User Use case so that, upon successful storage, calls a new Use Case.

: This new Use Case is in charge of sending the body and addressee of an email to an email sender interface adapter.[^flow]

: Create an interface adapter that uses the data produced by the  use case and sends it to an external queue[^celery], in the form of a message, that should send the email.

These stories are somewhat vague, and that is deliberate. I don't want to restrict—and not only because I would be restricting myself—and details of implementation are what code reviews and tests are for. The one exception I make on not specifying implementation is regarding the tech stack itself: it's such a big decision that all developers are benefitted if the stack is clear[^caveat].

The stories should only define a rough end goal, and I believe the ones I wrote here achieve that. Anyhow, I feel that this is a good first step and a general description of how we'll be working on this project.

This is going to be part of a series, an idea born from a [great article on blogging][blogging] that I read the other day, which inspired me to write more and gave me the idea of how to actually write: I'm going to push myself into working on this application (and refactoring an older one, with another friend) so that I have material to write for this blog, and I can use the will to write for the blog as incentive to work on those projects, killing two birds with one stone.

**IMPORTANT**: Everything I'm writing in these series is my interpretation and general idea of a good process. Anything (or everything) I write might be entirely wrong and, in such event, I encourage you to correct me in the comments.

[^jira]: Just FYI, I don't hate it, it can be a great tool, as long as it isn't drowned in the bastardization of scrum, which I don't hate either... as long as it's used as a guideline instead of a forced two-week waterfall grind.
[^arch]: I'm trying to describe this within the terms of the [clean architecture][architecture]. Results may vary.
[^cases]: And debatably at any stage. I've seen projects where stories are created for everything, even changing the color of a button to a slightly differen shade of blue. YMMV on advantages and disadvantages of that practice.
[^postgres]: I'm a postgreSQL user.
[^flask]: Probably a function that would retrieve the data in a given format, create a domain entity object from it that would then pass this object into the database adapter, probably a SQLAlchemy model. This function itself would be called from a [flask][] endpoint.
[^web]: I've worked as a full stack web developer almost exclusively, so in here I'm thinking of a form, created either from a JS framework or just a simple web form.
[^server]: Of course, nobody is forced to use a client-server system, but it's what I'll use.
[^dance]: Probably something like [flask-dance][].
[^clean]: Remember not to pollute the business rules or the entities with data or steps specific to any third party.
[^flow]: Remember not to break flow of control, these business rules don't care how the database signals success or how the sender adapter sends the message. But that's an implementation detail that should be discussed in review.
[^celery]: Probably rabbitmq through Celery.
[^caveat]: Everything beyond that (meaning *how* the stack is used) is outside the scope of the story. That's for tests and reviews.

[blogging]: //flaviocopes.com/blog-seo/
[belt]: //oceanservice.noaa.gov/facts/conveyor.html
[manifesto]: //agilemanifesto.org/
[sourcehut]: //sourcehut.org/
[architecture]: //blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html
[flask]: //www.palletsprojects.com/p/flask/
[flask-dance]: //flask-dance.readthedocs.io/en/latest/

*[overly elaborate metaphor]: sorry
*[application has a domain]: excuse me being captain obvious
*[encourage]: read: beg

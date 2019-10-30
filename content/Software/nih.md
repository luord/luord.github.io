title: The Not-Invented-Here syndrome
tags: process, development, concepts, musings, python, flask
summary: On creating own solutions versus implementing existing libraries or methods.
status: published
date: 2016-06-25

I read a while ago about the NIH syndrome and how it's generally not recommended because it unnecessarily increases the workload and the amount of code that needs to be maintained. Not to mention that using existing libraries or frameworks, specially open source ones, can also eventually involve helping the community and, thus, improving the code for everyone.

So, the recommendation is generally reusing as much code as possible, hopefully keeping the amount of original code reduced to the actual business logic of the project at hand. I think this is sound, but there's something to be said about producing in-house code and reinventing the wheel a little.

In my last official project, where I worked as a backend developer for a startup, we did use frameworks for all of backend, frontend and presentation, as well as several plugins for the frameworks to avoid increasing the workload too much, but we also wrote a lot of code that we might have found in existing libraries if we looked.

For a lot of the REST API, for example, I wrote all of the entrypoints and callback logic. I know now that proper usage of [Flask-Restful][] ([flask][] is, of course, my favorite framework) could have saved me a lot of work in that area... But I don't really regret it, I can say a learned a whole lot because I've always been a bit of a hands-on learner.

Of course, I've also seen first-hand that doing everything in-house can and does get out of control and, after a while, it becomes almost impossible for the handful of developers of a startup to maintain all that code.

In the project I'm working now, thanks to what I learned from writing a lot of my own code, it's been easier for me to research libraries and decide what would be a better fit as well as recognizing where I really do need to write; part of the reason I didn't reuse as much as I could in that other project was overestimating what was actual business logic and what were mere building blocks.

Given the chance, I'll probably refactor all that code and use Flask-Restful or similar to simplify it and make it more easily maintainable; but every learning opportunity is a good opportunity so I'm glad I went more zealous in the first go in that project.

What I'm trying to say is yes, one should avoid the NIH syndrome, surf the community, reuse stuff that hundreds if not thousands of people have polished (the more eyes, the better) and prevent getting the codebase from getting out of control due to reinventing the wheel. But one should also tackle at least one project where one writes as much code as possible, it highlights the importance of reusing the code in later projects, one gets first-hand experience on what leads people to write such libraries in the first place and, in general, one learns how the kind of projects one is working on generally work.

It goes without saying, of course, that doing such a thing is really only beneficial early in one's career. I see no reason for reinventing the wheel once one is already an experimented developer. Of course, someone more experienced than me could probably tell me otherwise.

In a different but related matter, in this website I've tried to avoid using frameworks of any kind; opting for more hands-on code. Just like doing it once helps to learn, I think that keeping a side, personal, project for practice keeps one from forgetting the basics. This site is, thus, my sandbox in a way, helping me practice HTML and Jinja templating (through the Pelican blog), LESS and CSS (for the themes, although I *am* using a theme I found) and plain JavaScript (for some behavior, like the discs in the [skills page][skills]).

[Flask-Restful]: //flask-restful.readthedocs.io/ "One of the best plugins for Flask"
[flask]: //palletsprojects.com/p/flask/ "Flask Framework"
[skills]: /pages/skills

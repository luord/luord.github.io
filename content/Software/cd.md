title: Continuous-delivery-with-Docker-and-Gitlab
tags: operations,development,gitlab,docker
summary: A rapid delivery pipeline using containers and gitlab ci. More than good enough for me.

Before working as a freelancer, just writing the code and tests and running everything manually before
deploying to staging and then production, also manually, was good enough. Now, however, with the potential
to work in several and vastly different projects and environments, this "process" has become increasingly
tedious and, as since I started working with Docker (by my own choice, like every other tool used in that project)
I've become more interested in operations, lately I tasked myself with automation of this.

After a while trying different things and the impossibility to work on others given that I'm a recent freelancer
with, thusly, limited income, I've settled in a process that I believe will suit me just fine, thanks to GitLab.com's
all-around awesomeness. It beats the other offerings I considered by a margin:

* Over GitHub, GitLab has private repositories in its free tier, something clients 'will' want, and also their built-in CI
* Over Google Cloud Repositories, GitLab has their integrated CI. It amazes me how GCR is almost completely isolated
from all other Google Cloud services. Apparently, they used to have a Push-to-Deploy feature, but that's gone (if it isn't,
it must be really well-hidden now because I spent days reading documentation, forums and question threads about this) and now
they suggest setting up one's own continuous integration service. I can't imagine why they did that and, again, having no money,
I'd rather not risk being charged for running their recommended Jenkins setup.
* Over Heroku (which I was reticent about anyway for different reasons), GitLab CI, being less opinionated,
offers more freedom in setting up the delivery process and allows itself to, upfront, deliver different types of applications easier.
* Over dedicated automation tools such as Jenkins of Buildbot, GitLab's CI has the advantage of being simpler and straightforward.
It might not be as maneuverable, but I believe what it offers is more than I need.

And, all this aside, GitLab CI works well with Docker, which I was already using for local development.
My development process is, now, roughly:

* Running docker containers (built with `docker-compose`) locally.
* Using git hooks (set in place using a bash script) to trigger tests.
* Pushing to GitLab, where their CI will take charge of running tests again and, on success, pushing to wherever was setup.

Right now, I'm pushing to Google App Engine, whose free tier, despite what's mentioned above, is still the best option for me.

## Preparation

For this guide one needs to have one account in [GitLab.com][gitlab] (or one's own GitLab server) and [Google Cloud][google] (or
one'll have to adjust to the vendor of choice).

Also, one needs to have [docker][], [docker-compose][], and [git][] installed locally.

## Code

The app will be a simple "Hello World" in [Flask][] with the following folder structure:

    app
    | - app.yaml
    | - docker-compose.yml
    | - .gitlab-ci.yml
    | - app
    |   | - __init__.py
    |   | - app.py
    |   | - Dockerfile
    |   | - requirements.txt

`app.py` is within a module and not in the root folder (which would be simpler) for ease of deployment to Google App Engine. This is its code:

    :::python
    from flask import Flask

    app = Flask(__name__)

    @app.route('/')
    def hello():
        return 'Hello World!'

    if __name__ == "__main__":
        app.run(host="0.0.0.0", debug=True)

`__init__.py` has the GAE path setup:

    :::python
    import os, sys

    lib_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'lib')
    sys.path.insert(0, lib_path)

    from .app import app

    if __name__ == "__main__":
        app.run()

The app only has one dependency, `flask`, and that word is the content of `requirements.txt` (not versioning your dependencies is, of course, not recommended).

Now the stuff this guide is meant to be about. First the `Dockerfile`:

    :::docker
    FROM python:latest

    ADD . /code

    WORKDIR /code

    RUN pip install -r requirements.txt

    CMD ["python","app.py"]

Simple enough: from the python image install the requirements and then run the server directly.

`docker-compose.yml` is very simple too:

    :::yaml
    app:
        build: app
        ports:
            - "5000:5000"

Build and run what's in the `app` folder

Now what allows GitLab to perform its magic, the `.gitlab-ci.yml` file:

    :::yaml
    back:
        image: python
        stage: build
        script:
            - pip install -t app/lib -r app/requirements.txt
        artifacts:
            paths:
                - app/lib/

    deploy_production:
        image: google/cloud-sdk
        stage: deploy
        environment: production
        only:
            - master
        script:
            - echo $GAE_KEY > /tmp/gae_key.json
            - gcloud config set project $GAE_PROJECT
            - gcloud auth activate-service-account --key-file /tmp/gae_key.json
            - gcloud --quiet app deploy
        after_script:
            - rm /tmp/gae_key.json

There are a couple things happening here, but nothing overly complicated:

* In the build stage, run the python docker image and install the requirements locally in a folder called `lib`. Make this folder available for next stages.
* In the deployment stage... deploy the app to GAE.

There a couple of environment variables used here. We'll see how to set them soon.

(Note: The script for `deploy_production` is partly based on the one in [this][attr] cool post by Dennis Alund).

Finally, `app.yaml`, which is specific to GAE:

    :::yaml
    runtime: python27
    threadsafe: true

    handlers:
        -   url: /
            script: app.app

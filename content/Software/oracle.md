title: Oracle in Docker
tags: operations,development,oracle,docker,guides,tutorials
summary: Using the official oracle docker images in development
image: /assets/img/oracle/dorac.jpg
date: 2017-11-13
status: published

A while ago, I had to work in a project that used oracle as its data layer (yeah, I know...).
When we started, there was no such thing as an Oracle docker image so the development environment
was either set-up manually or using bash scripts. I tried to create images but, first, it was hell and, second, I didn't want to
bother with any license breach. I love bash and I'm often scripting away repetitive stuff
but I am way too used to docker for my development environments (and also for deploying and in production);
as such, it can be said that, whenever I had to rebuild the environment from scratch (and since a migration was being
made towards data warehouses, that was more often than usual), I cursed my days.

Thankfully, by the time we were finishing and regressions were becoming more and more expected, [Oracle released
official images to the docker store][oracle]. I didn't waste time and, with some effort as the documentation
was quite sparse, I managed to set them up locally and turned the bash scripts (and some plain
text instructions) and other requirements into a `docker-compose` file. This short guide is about duplicating
the process (well, the Oracle part).

## Initial steps

First of all, create an account in the [docker store][docker] if you don't have one already.

Next, login with your account in the docker console, using the command `docker login`.

## Getting Oracle

With that set up, head over to the [oracle enterprise page][oradocker] in the docker store and click in the
button that says "*Proceed to Checkout*".

At this point, fill the information requested and accept the terms, the process is similar to the one Oracle has for downloading the
client and databases from their website. They require it here too because this is Oracle.

*Now* you can pull the docker image: `docker pull store/oracle/database-enterprise:12.2.0.1`. It'll take a while.

## Using Oracle

At this point you're probably in the instructions page, which is now far more detailed than it was when the images were released,
lucky you. They are relatively easy to follow but I'll write the last few commands required to use the image here anyway.

To start the image:

    docker run -d -it --name <db-container-name> store/oracle/database-enterprise:12.2.0.1

To connect to the database using Oracle's sqlplus client:

    docker exec -it <db-container-name> bash -c "source /home/oracle/.bashrc; sqlplus /nolog"

## Some options

* Setting the `DB_SID` environment variable changes the name of the database. Default is `ORCLCDB`.
* The port `1521` can be mapped so that the container can be accessed from the host. It can also, of course, be linked or set up in a network with other containers.
* The data can be separated in a volume, the directory to be mapped is `/ORCL`.
* Remember to change the password of the `sys` user (default is `Oradoc_db1`). This probably should be done in a Dockerfile that
uses this image as base.
* There's a smaller image (`store/oracle/database-enterprise:12.2.0.1-slim`) whose Oracle installation has fewer options and tools.
This is what I'd probably use if I have to work with Oracle again.

And that's it for now. If you have any problems or corrections, let me know in the comments!

[oracle]: //www.oracle.com/corporate/pressrelease/docker-oracle-041917.html
[docker]: //store.docker.com/
[oradocker]: //store.docker.com/account/confirm-email/abea38b5a9f5c26347324ff39a4b69b17f4e5dcf/?ref=oracle-database-enterprise-edition

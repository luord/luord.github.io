title: Automated initial OS setup
status: published
date: 2024-12-08 00:19

This weekend I finally got done something I probably should have back since I
got my first computer nearly two decades ago: a script to automate the initial
setup of a new OS installation. After all, I've been using Linux for most of
that time and it wasn't even that hard to do. I guess I never felt fully
confident in my setup itself to bother replicating it.

The biggest hurdle was that I have also always wanted synchronization
of my most valuable files across all my devices... Which I finally got done
this time too in a simple enough way, just how I like it. Sure, it's always
been possible, but nice tools like [rclone](https://rclone.org/) bisync and
[tailscale](https://tailscale.com/) make it significantly easier nowadays.

The script is [here](https://github.com/luord/scripts/blob/master/setup.sh).
It ended up being a handy opportunity to practice my Bash too, and it's
working pretty well for a minimalist like me. Still, suggestions are welcome!

# codestyle
code style for Wiren Board software

Lintian
-------

This directory contains wirenboard profile for lintian. It reconfigures some
checks to run in Jenkins pipelines after package builds (e.g. to check
changelog syntax and fail if there are syntax errors).

Currently this profile is used with lintian 2.5.50.4 from Debian stretch.
It may require some modifications when lintian will update.

Copy lintian directory into $HOME/.lintian and run lintian with parameters:

  $ lintian --include-dir=$HOME/.lintian --profile=wirenboard ...

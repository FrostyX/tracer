Tracer
======

DESCRIPTION
-----------

Tracer simply finds all packages that you have modified since you boot up. Then he traces their files loaded to the memory. As output, you will get list of applications what have been running while you updated or removed them.


OPTIONS
-------

GENERAL
~~~~~~~
::

    --version             print program version

    -h, --help            show this help message and exit

    -q, --quiet           do not print additional information

    -v, --verbose         print more informations. Use -v or -vv

MODES
~~~~~
::

    --helpers             not list applications, but list their helpers

    -i, --interactive     run tracer in interactive mode. Print numbered
                          applications and give helpers based on numbers

    -s app_name [app_name ...], --show app_name [app_name ...]
                          show helper for given application

    -a, --all             list even session and unrestartable applications

    -t TIMESTAMP, --timestamp TIMESTAMP
                          since when the updates should be

    -n, --now             when there are specified packages, dont look for time
                          of their update. Use "now" instead

USERS
~~~~~
::

    -u username, --user username

    -r, --root

    -e, --everyone


EXAMPLES
--------

::

    Show informations about application
        tracer --show mysqld

    Show even affected files of the application
        tracer --show mysqld -vv

    In interactive mode show all applications modified only through packages changed since timestamp
        tracer -iat 1414248388.04

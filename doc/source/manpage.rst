Tracer
======

DESCRIPTION
-----------

Tracer determines which applications use outdated files and prints them. For special kind of applications such as services or daemons, it suggests a standard command to restart it. Detecting whether file is outdated or not is based on a simple idea. If application has loaded in memory any version of a file which is provided by any package updated since system was booted up, tracer consider this application as outdated.


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

    --daemons-only, --services-only
                          list only daemons/services

    --hooks-only          do not print traced applications, only run their hooks

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

DEBUG
~~~~~
::

    --show-resource=<option>
                          options: packages | processes | rules | applications | system
                          dump informations that tracer can use

EXIT CODES
----------
::

  Status codes and their meanings:

  +-------------+----------------------------------+
  | Status code | Meaning                          |
  +=============+==================================+
  | 1-99        | Error exit codes                 |
  +-------------+----------------------------------+
  | 0           | No affected applications         |
  +-------------+----------------------------------+
  | 101         | Found some affected applications |
  +-------------+----------------------------------+
  | 102         | Found some affected daemons      |
  +-------------+----------------------------------+
  | 103         | Session restart needed           |
  +-------------+----------------------------------+
  | 104         | Reboot needed                    |
  +-------------+----------------------------------+


EXAMPLES
--------

::

    Show your applications which needs restarting (basic usage)
        tracer

    Show informations about application
        tracer --show mysqld

    Show even affected files of the application
        tracer --show mysqld -vv

    In interactive mode show all applications modified only through packages changed since timestamp
        tracer -iat 1414248388.04

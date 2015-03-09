Tracer
======

Tracer finds outdated running applications in your system

Tracer determines which applications use outdated files and prints them. For special kind of applications such as services or daemons, it suggests a standard command to restart it. Detecting whether file is outdated or not is based on a simple idea. If application has loaded in memory any version of a file which is provided by any package updated since system was booted up, tracer consider this application as outdated.

Docs
----

.. toctree::
   :maxdepth: 1

   Home <self>
   user-guide
   developer-guide
   get-tracer
   Manpage <manpage>
   api

Feedback
--------

Please report any bugs or feature requests to `issues`_ on this repository. Pull requests are also welcome, but please visit :doc:`developer-guide` first. If you rather want a talk or something, you can find me on ``#gentoo.cs`` or ``#fedora-cs`` ``@freenode`` or you can mail me to frostyx@email.cz.


.. _coveralls: https://coveralls.io/r/FrostyX/tracer?branch=master
.. _travis: https://travis-ci.org/FrostyX/tracer
.. _issues: https://github.com/FrostyX/tracer/issues

Tracer API
==========

Tracer provides a small interface that you can use in your application. It consist from ``Query`` class which is able to
ask Tracer for various informations and provide you a results. And from data structues from which results consists.

Surely you could access internal classes and methods on your own, but there is a risk that they will change in the
future. In API could be a little changes too, but they will be documented

Querying
--------

.. autoclass:: tracer.Query
    :members:


Hooks
-----

Tracer also provides API for user-defined hooks. They can be defined as a simple functions decorated by
``@hooks.match("app_name")``. Tracer will search for them in directories ``~/.config/tracer/hooks/``
and ``/etc/tracer/hooks/``. Such hook will be called when tracer determines, that linked application needs restarting.

.. autofunction:: tracer.hooks.match

.. note::
   If you want to run tracer's hooks and print no other output, use ``tracer --hooks-only``


Exit codes
----------

In some use-cases you may want to examine Tracer's results through exit codes (also known as status codes). See their
meanings:

=======  ================================
1-99     Error exit codes
0        No affected applications
101      Found some affected applications
102      Found some affected daemons
103      Session restart needed
104      Reboot needed
=======  ================================


Data structures
---------------

Follows list of classes which quering results may consist from. Not all their properties are covered within API. If your
use case requires some which are not listed below, please let me know to cover them in API too.

Packages
~~~~~~~~

.. autoclass:: tracer.Package
   :members:


Applications
~~~~~~~~~~~~

.. autoclass:: tracer.Application
   :members:
   :exclude-members: processes_factory helper

.. autoclass:: tracer.Process
   :inherited-members:
   :members:
   :exclude-members: str_started_ago

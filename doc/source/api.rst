Tracer API
==========

Tracer provides a small interface that you can use in your application. It consist from ``Query`` class which is able to
ask Tracer for various informations and provide you a results. And from data structues from which results consists.

Surely you could access internal classes and methods on your own, but there is a risk that they will change in the
future. In API could be a little changes too, but they will be documented

Quering
-------

.. autoclass:: tracer.query.Query
    :members:


Data structures
---------------

Follows list of classes which quering results may consist from. Not all their properties are covered within API. If your
use case requires some which are not listed below, please let me know to cover them in API too.

Packages
~~~~~~~~

.. autoclass:: tracer.resources.package.Package
   :members:


Applications
~~~~~~~~~~~~

.. autoclass:: tracer.resources.applications.Application
   :members:
   :exclude-members: processes_factory helper

.. autoclass:: tracer.resources.processes.Process
   :inherited-members:
   :members:
   :exclude-members: str_started_ago

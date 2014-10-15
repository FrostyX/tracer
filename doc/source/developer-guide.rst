Developer Guide
===============

Python
------

Tracer is build on Python 2.7 because this version is most spread on linux systems. Besides basic python, tracer requires its few packages:

- `psutil`_ - For getting informations about processes, memory, etc
- `beautifulsoup`_ - For parsing user defined xml files such as ``data/applications.xml`` and ``data/rules.xml``

Coding style
------------

If you want to contribute and write some code, I will strictly insist on these rules

1. Use **tabs** for indentation

  - Tabs are meaningful - 1 tab = 1 logical level
  - Everyone can view the one same tab with different width
  - Easier to work with

2. Use **spaces** for aligning

  -  There is no way how to correctly align with tabs

3. Use ``camelCase`` for naming files, ``CamelCase`` for classes, ``underscore\_case`` for methods and variables
4. There are no access modifiers, so use prefix ``\_`` for private things

There is an example code following our coding style

.. code:: python

    class Rpm(IPackageManager):

        def packages_newer_than(self, unix_time):
            packages = []
            for t in self._transactions_newer_than(unix_time):
                # Append every package in transaction into `packages`
                ...
            return packages

        def _transactions_newer_than(self, unix_time):
            ...

Packaging
---------

Tracer uses `tito`_ for managing versions and doing all RPM stuff. There is quote what tito is:

    "Tito is a tool **for managing RPM based projects** using git for their source code repository"

That means if you are fedora user, you can use prepared ``tito`` package, but else you probably would have to install it by your own.

Next, there is `Makefile`_ describing most of actions you might want to do.

In general, managing versions

::

    make release

    # For specific version use
    tito tag --use-version X.Y.Z

Fedora
~~~~~~

::

    # Develop
    [1] make rpm-test
    [2] make rpm-try

    # Create official package
    [3] make rpm

-  [1] Create RPM package from last commit.
-  [2] Same as [1] but additionally install it.
-  [3] Create SRPM from last tag and ask `copr`_ to build RPM packages and distribute it through `frostyx/tracer`_ repository. There is ``.repo`` files for `F19`_ and `F20`_


.. _psutil: https://code.google.com/p/psutil/
.. _beautifulsoup: http://www.crummy.com/software/BeautifulSoup/bs4/doc/
.. _tito: https://github.com/dgoodwin/tito
.. _Makefile: https://github.com/FrostyX/tracer/blob/master/Makefile
.. _copr: https://copr.fedoraproject.org/coprs/
.. _frostyx/tracer: https://copr.fedoraproject.org/coprs/frostyx/tracer/
.. _F19: https://copr.fedoraproject.org/coprs/frostyx/tracer/repo/fedora-19-i386/frostyx-tracer-fedora-19-i386.repo
.. _F20: https://copr.fedoraproject.org/coprs/frostyx/tracer/repo/fedora-20-i386/frostyx-tracer-fedora-20-i386.repo

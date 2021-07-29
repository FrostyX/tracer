Get Tracer
==========

There are few ways how to get tracer. Recommended is installing it through linux distribution package, but so far there are only few supported ditributions and even less of them has tracer packaged. If you are unlucky and can’t find your system in the list, you can do three things.

1. Create and maintain tracer package for your ditribution
2. Request me to do it for you (but I don’t promise that I will)
3. Use tracer from git

Fedora
------

Fedora is intended as the primary system, so there shouldn’t be a problem. You can simply install tracer using

::

    dnf install tracer

Please note that for DNF also exists plugin which calls tracer after every successful transaction. You can install it using

::

    dnf install dnf-plugins-extras-tracer

Take a look into User Guide at :ref:`dnf-plugin`.


EPEL 8
------

The ``tracer`` package is available in the official repositories for
RHEL 8.4 and higher. As such, it can be easily installed with::

    dnf install tracer

There is also a Copr repository providing up-to-date stable builds for
EPEL8. It is recommended to use this repository for installing
Tracer on RHEL 8.3 and lower::

    dnf copr enable frostyx/tracer-epel
    dnf install tracer


Enterprise Linux 7 (CentOS, ect.)
---------------------------------

Tracer can be install from EPEL

::

    yum install epel-release
    yum install tracer 


Gentoo
------

So far I have ``tracer.ebuild`` in my `personal overlay`_. Please take note that *is not* properly packaged - it just clone the git repository. However it has one relevant advantage and that is that it takes care about dependencies.

::

    layman -a frostyx
    emerge tracer


ArchLinux
---------

An unofficial tracer package can be found in the `AUR`_: https://aur.archlinux.org/packages/tracer

Git
---

You can download the code by running this command:

::

    git clone git@github.com:FrostyX/tracer.git


1) Manuall installation
~~~~~~~~~~~~~~~~~~~~~~~

First of all check tracer's `requirements`_ and install them.

Now you should be able to run it by ``tracer/bin/tracer.py``, but becaue it is so unhandy I will recommend you to make symlink into ``$PATH`` directory. For instance

::

    sudo ln -s tracer/bin/tracer.py /usr/local/bin/tracer

and then run it just by ``tracer`` command.

2) Automated installation
~~~~~~~~~~~~~~~~~~~~~~~~~

Previous paragraph can be done by running

::

    sudo pip install ./tracer/
    # or
    pip install --user ./tracer/


.. _F19: https://copr.fedoraproject.org/coprs/frostyx/tracer/repo/fedora-19-i386/frostyx-tracer-fedora-19-i386.repo
.. _F20: https://copr.fedoraproject.org/coprs/frostyx/tracer/repo/fedora-20-i386/frostyx-tracer-fedora-20-i386.repo
.. _personal overlay: https://github.com/frostyx/gentoo-overlay
.. _requirements: https://github.com/FrostyX/tracer#requirements
.. _AUR: https://wiki.archlinux.org/index.php/Arch_User_Repository

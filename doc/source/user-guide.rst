User Guide
==========

Installation
------------

Please, see how to :doc:`get-tracer`.

Standard usage
--------------

Standard way to use tracer is just running the ``sudo tracer`` command. I am working on user-only mode, but in this moment it runs only with root permissions (It needs access to your package manager’s history). There you can see the output:

::

    $[FrostyX  ~]-> sudo tracer
    You should restart:
      * Some applications using:
          sudo service apache2 restart
          sudo service mpd restart

      * These applications manually:
          chromium
          dolphin
          gvim

    Additionally, there are:
      - 6 processes requiring restarting your session (i.e. Logging out & Logging in again)
      - 2 processes requiring reboot

As you can see, It hides few kinds of applications to not bothering you with such that you can’t control. But of course, if you want, you can see them all, use the ``-a`` or ``--all`` parameter.

Helpers
-------

You got list of applications, but what next. There is ``-s`` or ``--show`` parameter for showing some handy informations. It displays package owning this application, what user started it and when, its PID and recommended way, how to restart it. When you want to print helpers for all affected applications, you can use ``--helpers`` parameter.

::

    $[FrostyX  ~]-> tracer -s apache2
    * apache2
        Package:     www-servers/apache
        Description: The Apache Web Server.
        Type:        Daemon
        State:       apache2 has been started by root 34 minutes ago. PID - 18816

        How to restart:
             service apache2 restart

Helpers for custom applications can be defined in ``/etc/tracer/applications.xml`` & ``~/.config/tracer/applications.xml``. If you have any objections to the described way how to restart it, please `create an issue`_.

Interactive mode
----------------

Printing helper for specific application is handy but not for every situation. For instance it can be little awkward to call ``tracer -s app_name`` a lot of specific applications. That would be lot of boring and senseless typing so I am introducing interactive mode to you.

When you use ``-i`` or ``--interactive``, tracer will print number next to every application. Then you will be asked for input. That is simple way how to iterate through helpers for all applications.

::

    $[FrostyX  ~]-> sudo tracer -i
    [1] gvim
    [2] mpd
    [3] dolphin
    [4] apache2

    Press application number for help or 'q' to quit
    --> 2
    * mpd
        Package:     media-sound/mpd
        Description: The Music Player Daemon (mpd)
        Type:        Daemon
        State:       mpd has been started by frostyx 23 hours ago. PID - 3751

        How to restart:
             service mpd restart

    -- Press enter to get list of applications --

Verbose
-------

Like most of UNIX programs, even tracer has ``verbose`` mode. It provides three levels of chattiness.

Non-verbose mode

::

    $[FrostyX  ~]-> sudo tracer -s gvim
    * gvim
        Package:     app-editors/gvim
        Description: GUI version of the Vim text editor
        Type:        Application
        State:       gvim has been started by frostyx 2 hours ago. PID - 8431

        How to restart:
            Sorry, It's not known

First verbose level

::

    $[FrostyX  ~]-> sudo tracer -s gvim -v
    * gvim
        Package:     app-editors/gvim
        Description: GUI version of the Vim text editor
        Type:        Application
        State:       gvim has been started by frostyx 2 hours ago. PID - 8431

        Affected by:
            gnome-base/gvfs
            x11-libs/libX11

        How to restart:
            Sorry, It's not known

Second verbose level

::

    $[FrostyX  ~]-> sudo tracer -s gvim -vv
    * gvim
        Package:     app-editors/gvim
        Description: GUI version of the Vim text editor
        Type:        Application
        State:       gvim has been started by frostyx 2 hours ago. PID - 8431

        Affected by:
            gnome-base/gvfs
                /usr/lib/gvfs/libgvfscommon.so
                /usr/lib/gio/modules/libgioremote-volume-monitor.so
                /usr/lib/gio/modules/libgvfsdbus.so
            x11-libs/libX11
                /usr/lib/libX11.so
                /usr/lib/libX11-xcb.so

        How to restart:
            Sorry, It's not known

Distro-specific candy
---------------------

.. _dnf-plugin:

Fedora - DNF plugin
~~~~~~~~~~~~~~~~~~~

There is plugin for new fedora package manager - DNF. It calls tracer after every successful transaction. Please note that it checks only packages in actual transaction, so if you run ``tracer`` from command line, you can actually get longer list.

If you want this feature, install the plugin package. Please notice that there are two of them. For F21 and higher install the ``dnf-plugins-extras-tracer``. If you are still using F20, please install ``dnf-plugin-tracer``, but be aware that this package is obsoleted and will be no new versions of it.

::

    $[FrostyX  ~]-> sudo dnf update vim-X11
    ...
    Running transaction
      Upgrading    : vim-common-2:7.4.179-1.fc20.i686                           1/6
      Upgrading    : vim-X11-2:7.4.179-1.fc20.i686                              2/6
      Upgrading    : vim-enhanced-2:7.4.179-1.fc20.i686                         3/6
      ...

    Upgraded:
      vim-X11.i686 2:7.4.179-1.fc20           vim-common.i686 2:7.4.179-1.fc20
      vim-enhanced.i686 2:7.4.179-1.fc20

    You should restart:
      gvim

    Done!

If you can’t see tracer section in your output, make sure that in your ``/etc/dnf/dnf.conf`` is not ``plugins=0`` or specified `pluginpath`_ to different than default directory.

Error occured
-------------

Some weird error occured! What should I do? Please keep calm and read it. There should be information what can be wrong and how you can deal with it. For instance

::

    frostyx@kubuntu:~$ sudo tracer
    You are running unsupported linux distribution

    Please visit https://github.com/FrostyX/tracer/issues
    and create new issue called 'Unknown or unsupported linux distribution: Ubuntu' if there isn't such.

    Don't you have an GitHub account? Please report this issue on frostyx@email.cz

There is little possibility that you can encounter different type of error. Something like this

::

    Traceback (most recent call last):
      File "/usr/local/bin/tracer", line 169, in <module>
        main()
      File "/usr/local/bin/tracer", line 56, in main
        if args.interactive: _print_all_interactive(processes)
      File "/usr/local/bin/tracer", line 88, in _print_all_interactive
        answer = raw_input("--> ")

It is python traceback. My apologies, you shouldn’t see it. The best thing you can do, is openning new issue in `tracer’s issue tracker`_. Please describe how can I reproduce this issue or what did you do when error occured. Please post complete error message too.

Troubleshooting
---------------

Only root can use this application
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As I described above, tracer works only with root permissions so far.

You are running unsupported linux distribution
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Please read rest of that message. It describes what you can do

.. _pluginpath: http://akozumpl.github.io/dnf/api_conf.html#dnf.conf.Conf.pluginpath
.. _tracer’s issue tracker: https://github.com/FrostyX/tracer/issues
.. _create an issue: https://github.com/FrostyX/tracer/issues

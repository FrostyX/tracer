# tracer

Tracer finds outdated running applications in your system

How does he do it? He simply finds all packages you have modified since you boot up. Then he traces their files in the jungle of your memory, ... senses them, and finally, finds them. In the end you will get list of packages what have been running while you updated or removed them.

## Requirements
- Supported linux distribution - There are currently supported [Fedora](http://fedoraproject.org/) and [Gentoo](http://www.gentoo.org/)
- Python interpreter
- Python [psutil](https://code.google.com/p/psutil/) module. Available [here](https://admin.fedoraproject.org/pkgdb/acls/name/python-psutil) and [here](https://packages.gentoo.org/package/dev-python/psutil). Please use testing version on gentoo.

## Usage
### Basics
Clone tracer from GitHub

	git clone git@github.com:FrostyX/tracer.git

And simply run it

	sudo ./tracer/bin/tracer.py

_Yeah, you really have to run it as root._

### Symlink in PATH
Since there is no installation method so far, you can make symlink of `bin/tracer.py` to your `PATH` directory by yourself. Then you can use `tracer` just by calling its name.

	# Make symlink
	sudo ln -s tracer/bin/tracer.py /usr/local/bin/tracer

	# And then just run
	sudo tracer

### Arguments and pipes
You can also specify packages that *only* should be traced. Just pass them as arguments [1] or pipe them into `tracer` [2] \(or combine them\)

	# [1]
	sudo tracer mpd ncmpcpp vim

	# [2]
	echo mpd ncmpcpp vim | sudo tracer


## Integration with package managers
### DNF
Make symlink of `integration/dnf/plugins/tracer.py` file to your [dnf plugin directory](http://akozumpl.github.io/dnf/api_conf.html#dnf.conf.Conf.pluginpath)

Tracer is called after every successful transaction.

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

	Calling tracer
	vim-X11

	Done!

If you cant see tracer section in your output, make sure that you don't have `plugins=0` in your `/etc/dnf/dnf.conf`.


## Feedback
Please report any bugs or feature requests to [issues](https://github.com/FrostyX/tracer/issues) on this repository. Pull requests are also welcome. If you rather want a talk or something, you can find me on `#gentoo.cs` or `#fedora-cs` `@freenode` or you can [mail me](mailto:frostyx@email.cz).

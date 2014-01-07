# tracer

Tracer finds outdated running packages in your system

How does he do it? He simply finds all packages you have modified since you boot up. Then he traces their files in the jungle of your memory, ... senses them, and finally, finds them. In the end you will get list of packages what have been running while you updated or removed them.

## Requirements
- Supported linux distribution - There are currently supported [Fedora](http://fedoraproject.org/) and [Gentoo](http://www.gentoo.org/)
- Python interpreter
- Python [psutil](https://code.google.com/p/psutil/) module. Available [here](https://admin.fedoraproject.org/pkgdb/acls/name/python-psutil) and [here](https://packages.gentoo.org/package/dev-python/psutil). Please use testing version on gentoo.

## Usage
Clone tracer from GitHub

	git clone git@github.com:FrostyX/tracer.git

And simply run it

	sudo ./tracer/bin/tracer.py

_Yeah, you really have to run it as root._


## Feedback
Please report any bugs or feature requests right [here](https://github.com/FrostyX/tracer/issues) on GitHub. Pull requests are also welcome. If you rather want a talk or something, you can find me on `#gentoo.cs` or `fedora-cs` `@freenode` or you can [mail me](mailto:frostyx@email.cz).

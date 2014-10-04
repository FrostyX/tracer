# tracer [<img src="https://travis-ci.org/FrostyX/tracer.svg?branch=master" alt="Travis" align="right">](https://travis-ci.org/FrostyX/tracer)

Tracer finds outdated running applications in your system

How does he do it? He simply finds all packages you have modified since you boot up. Then he traces their files in the jungle of your memory, ... senses them, and finally, finds them. In the end you will get list of packages what have been running while you updated or removed them.


## Features
- [Find outdated running applications](https://github.com/FrostyX/tracer/wiki/User-Guide#standard-usage)
- [Show application informations and recommend a way how to restart it](https://github.com/FrostyX/tracer/wiki/User-Guide#helpers)
- [Integration with DNF](https://github.com/FrostyX/tracer/wiki/User-Guide#fedora---dnf-plugin)
- Specify a list of applications what should it look for (by pipe or arguments)
- List applications and interactively show informations

Please see [User Guide](https://github.com/FrostyX/tracer/wiki/User-Guide)

## Requirements
- Supported linux distribution - There are currently supported [Fedora](http://fedoraproject.org/), [Gentoo](http://www.gentoo.org/) and [Debian](https://www.debian.org/)
- Python interpreter
- Python [psutil](https://code.google.com/p/psutil/) module. Available [here](https://admin.fedoraproject.org/pkgdb/acls/name/python-psutil) and [here](https://packages.gentoo.org/package/dev-python/psutil). Please use testing version on gentoo.
- Python [beautifulsoup](http://www.crummy.com/software/BeautifulSoup/bs4/doc/) module. Available [here](https://admin.fedoraproject.org/pkgdb/acls/name/python-beautifulsoup4) and [here](https://packages.gentoo.org/package/dev-python/beautifulsoup)


## Feedback
Please report any bugs or feature requests to [issues](https://github.com/FrostyX/tracer/issues) on this repository. Pull requests are also welcome, but please visit [Developer Guide](https://github.com/FrostyX/tracer/wiki/Developer-Guide) first. If you rather want a talk or something, you can find me on `#gentoo.cs` or `#fedora-cs` `@freenode` or you can [mail me](mailto:frostyx@email.cz).


## References
- <https://pythonhosted.org/psutil/>
- <https://code.google.com/p/psutil/wiki/Documentation>
- <https://docs.python.org/2/library/unittest.html>

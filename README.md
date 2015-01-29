# Tracer [<img src="https://coveralls.io/repos/FrostyX/tracer/badge.png?branch=master" alt="Coverage Status" align="right">](https://coveralls.io/r/FrostyX/tracer?branch=master)[<img src="https://travis-ci.org/FrostyX/tracer.svg?branch=master" alt="Travis" align="right">](https://travis-ci.org/FrostyX/tracer)

Tracer finds outdated running applications in your system

Tracer determines which applications use outdated files and prints them. For special kind of applications such as services or daemons, it suggests a standard command to restart it. Detecting whether file is outdated or not is based on a simple idea. If application has loaded in memory any version of a file which is provided by any package updated since system was booted up, tracer consider this application as outdated.

## Overview
<table frame="void" rules="none">
	<tbody valign="top">
		<tr>
			<th>Website:</th>
			<td><a href="http://tracer-package.com">http://tracer-package.com</a></td>
		</tr>
		<tr>
			<th>Source:</th>
			<td><a href="https://github.com/FrostyX/tracer">https://github.com/FrostyX/tracer</a></td>
		</tr>
		<tr>
			<th>Documentation:</th>
			<td><a href="http://docs.tracer-package.com">http://docs.tracer-package.com</a></td>
		</tr>
		<tr>
			<th>License:</th>
			<td>GNU GPL v2.0</td>
		</tr>
	</tbody>
</table>

## Features
- [Find outdated running applications](http://docs.tracer-package.com/en/latest/user-guide/#standard-usage)
- [Show application informations and recommend a way how to restart it](http://docs.tracer-package.com/en/latest/user-guide/#helpers)
- [Integration with DNF](http://docs.tracer-package.com/en/latest/user-guide/#fedora-dnf-plugin)
- Specify a list of applications what should it look for (by pipe or arguments)
- List applications and interactively show informations

Please see [User Guide](http://docs.tracer-package.com/en/latest/user-guide/)

## Requirements
- Supported linux distribution - There are currently supported [Fedora](http://fedoraproject.org/), [Gentoo](http://www.gentoo.org/) and [Debian](https://www.debian.org/)
- Python interpreter
- Python [psutil](https://code.google.com/p/psutil/) module. Available [here](https://admin.fedoraproject.org/pkgdb/acls/name/python-psutil) and [here](https://packages.gentoo.org/package/dev-python/psutil).
- Python [beautifulsoup](http://www.crummy.com/software/BeautifulSoup/bs4/doc/) module. Available [here](https://admin.fedoraproject.org/pkgdb/acls/name/python-beautifulsoup4) and [here](https://packages.gentoo.org/package/dev-python/beautifulsoup)


## Feedback
Please report any bugs or feature requests to [issues](https://github.com/FrostyX/tracer/issues) on this repository. Pull requests are also welcome, but please visit [Developer Guide](http://docs.tracer-package.com/en/latest/developer-guide/) first. If you rather want a talk or something, you can find me on `#gentoo.cs` or `#fedora-cs` `@freenode` or you can [mail me](mailto:frostyx@email.cz).


## References
- <https://pythonhosted.org/psutil/>
- <https://code.google.com/p/psutil/wiki/Documentation>
- <https://docs.python.org/2/library/unittest.html>

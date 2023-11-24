# Tracer

Tracer finds outdated running applications in your system

Tracer determines which applications use outdated files and prints
them. For special kind of applications such as services or daemons, it
suggests a standard command to restart it. Detecting whether file is
outdated or not is based on a simple idea. If application has loaded
in memory any version of a file which is provided by any package
updated since system was booted up, tracer consider this application
as outdated.


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
			<td><a href="https://tracer.readthedocs.io/">https://tracer.readthedocs.io/</a></td>
		</tr>
		<tr>
			<th>License:</th>
			<td>GNU GPL v2.0</td>
		</tr>
	</tbody>
</table>


## Status

| CI       | Badge                                                        |
| -------- | ------------------------------------------------------------ |
| Coverage | [![Coverage status][badge-coverage-img]][badge-coverage-url] |
| Travis   | [![Travis][badge-travis-img]][badge-travis-url]              |


## Features
- [Find outdated running applications][docs-standard-usage]
- [Show application informations and recommend a way how to restart it][docs-helpers]
- [Integration with DNF][docs-dnf-plugin]
- Specify a list of applications what should it look for (by pipe or arguments)
- List applications and interactively show informations

Please see [User Guide][docs-user-guide]


## Supported distributions

Tracer currently supports the following distributions.

- [Fedora](https://fedoraproject.org/)
- [Mageia](https://www.mageia.org/)
- [Gentoo](https://www.gentoo.org/)
- [Debian](https://www.debian.org/)
- [Arch](https://archlinux.org)

Their derivates might be supported as well, although some minor tweaks
might be necessary.


## Installation instructions

Please see [Installation instructions][docs-installation-instructions]
in the documentation.


## Feedback

Please report any bugs or feature requests to [issues][tracer-issues]
on this repository. Pull requests are also welcome, but please visit
[Developer Guide][docs-developer-guide] first. If you rather want a
talk or something, you can find me on `#gentoo.cs` or `#fedora-cs` at
`libera.chat` or you can [mail me](mailto:frostyx@email.cz).


## Similar software

- [needs-restarting](https://dnf-plugins-core.readthedocs.io/en/latest/needs_restarting.html)
- [oldprocs](https://github.com/gsauthof/utility/#oldprocs)
- [checkrestart](http://manpages.ubuntu.com/manpages/trusty/man1/checkrestart.1.html)
- [needrestart](https://github.com/liske/needrestart)



[badge-coverage-img]: https://coveralls.io/repos/FrostyX/tracer/badge.png?branch=master
[badge-coverage-url]: https://coveralls.io/r/FrostyX/tracer?branch=master
[badge-travis-img]: https://travis-ci.org/FrostyX/tracer.svg?branch=master
[badge-travis-url]: https://travis-ci.org/FrostyX/tracer
[docs-standard-usage]: https://tracer.readthedocs.io/en/latest/user-guide.html#standard-usage
[docs-helpers]: https://tracer.readthedocs.io/en/latest/user-guide.html#helpers
[docs-dnf-plugin]: https://tracer.readthedocs.io/en/latest/user-guide.html#fedora-dnf-plugin
[docs-user-guide]: https://tracer.readthedocs.io/en/latest/user-guide.html
[docs-developer-guide]: https://tracer.readthedocs.io/en/latest/developer-guide.html
[docs-installation-instructions]: https://tracer.readthedocs.io/en/latest/get-tracer.html
[tracer-issues]: https://github.com/FrostyX/tracer/issues

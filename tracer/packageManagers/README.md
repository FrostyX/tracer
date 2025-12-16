# Package managers

Every package manager module should inherit `IPackageManger` class and implement its methods:

- `packages_newer_than(self, unix_time)`
- `package_files(self, pkg_name)`
- `load_package_info(self, package)`
- `provided_by(self, app)`
- `package_name_only(self, pkg_object)`

Also there should be unit test for every package manager. Please see [dnf test](https://github.com/FrostyX/tracer/blob/develop/tests/test_dnf.py) for example.

# Package managers

Every package manager module should inherit `IPackageManger` class and implement `packages_newer_than(self, unix_time)` and `package_files(self, pkg_name)` methods. Also there should be unit test for every package manager.

# Changelog

This documents the changes in `bbf` releases. Version numbers follows [semantic
versioning](https://semver.org/).


## bbf-0.3.2

Fix several regressions introduced in `bbf-0.3.0`

* `BSpline` instances can be pickled
* Sparse matrices returned by `BSpline` instances are `csr_matrix` (was `csr_array`)
* Reintroduction of `BSpline.nj`


## bbf-0.3.1

* Bugfixes

  * Fixed a bug with `OpenMP` instructions in C code. The bug impacted the
    `clang` compiler while `gcc` compiled code was fine.


## bbf-0.3.0

* Improvments

  * Uses `nanobind` instead of `ctypes` to wrap the bsplines C extension. This
    allows for a simple cross-platforms installation of the package. See
    [#6](https://gitlab.in2p3.fr/lemaitre/bbf/-/issues/6).
  * Few unit tests (about bsplines) under continuous integration.


## bbf-0.2.0

First public release.

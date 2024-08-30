# tParton

This is an evolution code for the transversity parton distribution functions encountered in hadronic physics.

First, install this package using `pip install tparton`.

To evolve a transversity pdf, run the command `python -m tparton m`. This uses the Mellin moment by default. To use the energy scale integration method, run the command `python -m tparton t`. Use `python -m tparton m -h`/`python -m tparton t -h` for help.

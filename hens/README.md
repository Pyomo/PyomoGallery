The code works for:
  - python 3.5.2
  - Pyomo 5.0.1
  - PyLaTex 1.0.0 (optional)
  - Gurobi

There are two algorithms in directories:
  - ``adaptive_model_mixer``
  - ``beta_adaptive_model_mixer``

To find out how to use the code, run from terminal:
```sh
  cd <directory>
  python iterative.py -h
```
where ``directory`` is one of:
  - ``adaptive_model_mixer``
  - ``beta_adaptive_model_mixer``

To add your own datafile:
  put it in the ``datafiles`` directory and give it the extension ``.dat``
  e.g. if ``example.dat`` is in ``datafiles`` then
```sh
    cd adaptive_model_mixer
    python iterative.py example anyAlphaNumericThingCanGoHere
```
should work and a directory named ``example`` containing the results will be created.

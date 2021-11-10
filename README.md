# NEOS Optimization Command Line Tool

Command line tool for communicating with the NEOS optimization server, especially for
submitting optimization problems and retrieving optimization results.

## Installation

`neos` can be installed directly from this GitHub repository using `pip`:

```bash
pip install git+https://github.com/sebastianbaltser/neos
```

Installing will provide the `neos` command group which can be executed from the command line.

## Usage

Say for example that you defined the optimization problem in the three files `optim.mod`, `optim.dat`, 
and `optim.run`. The problem category is linear programming, and you would like to use the solver CPLEX.

To submit the optimization problem to the NEOS server navigate to the folder where the files are located, 
and use the `neos submit` command specifying the basename of the files:

```bash
neos submit "optim" --email your@email.com --category lp --solver CPLEX
```

If the files have different basenames, you can specify each separate name with extensions:

```bash
neos submit "ts_problem.mod" "ts_problem.run" "optim.dat" --email your@email.com --category lp --solver CPLEX
```

This will submit the job to the NEOS server and print the results when they are available.
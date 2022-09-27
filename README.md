# Display Tree

|               |                   |
|---------------|-------------------|
|   Author      |   Ethan Tan       |
|   Date        |   27/09/2022      |
|   Language    |   Python (py)     |

## Description

This package is meant to provide a high-level API for programmers to manage and visualise tree data structures easily.

## Setup

It is extremely easy to integrate this package in your existing projects.

In the command line, run:

```bash
pip install display-tree
```

_Note the package name uses dashes_

## Sample Usage

```python
from display_tree import Tree # Note the package name uses underscores

# Instantiate Parse Tree Object
t = ParseTree()

# Read a Mathematical String Expression (separated by singular whitespace characters)
t.read('1 + 2 * 3')

# Retrieve the Result
print('<<< Equation >>>')
print(t.expression, '=', t.evaluate(), end='\n\n')

# Display the Parse Tree
print('<<< Parse Tree >>>')
print(str(t))
```

The output in the terminal will look something like this:

```console
<<< Equation >>>
1 + 2 * 3 = 7

<<< Parse Tree >>>
 +
/  \
1  *
  / \
  2 3
```

## Tutorial

```
+---+---+---+
|   | A |   |
+---+---+---+
| / |   | \ |
+---+---+---+
| B |   | C |
+---+---+---+

    <---> padding = 1
```


## See Also

- [GitHub Source Code](https://github.com/ethanolx/Animated-Parse-Tree-py)
- [Full Documentation](https://github.com/ethanolx/Animated-Parse-Tree-py/wiki)
- [Python Package (PyPI)](https://pypi.org/project/animated-parse-tree)

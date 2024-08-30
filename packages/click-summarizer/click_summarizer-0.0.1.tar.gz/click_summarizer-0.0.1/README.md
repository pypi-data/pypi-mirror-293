# click-summarizer

[![PyPI - Version](https://img.shields.io/pypi/v/click-summarizer.svg)](https://pypi.org/project/click-summarizer)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/click-summarizer.svg)](https://pypi.org/project/click-summarizer)

-----

## Table of Contents

- [click-summarizer](#click-summarizer)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Usage: Command Line](#usage-command-line)
  - [Usage: Python](#usage-python)
  - [License](#license)

## Installation

```console
pip install click-summarizer
```


## Usage: Command Line

```console

click-summarizer --help
click-summarizer click_summarizer.cli summarize_cli

# Use it for other click-based cli apps.
click-summarizer dataset_sh.cli cli
click-summarizer dataset_sh.cli cli --no-doc
```

## Usage: Python

Assuming you have a click app like this:

```python
@click.group()
@click.option('--verbose', is_flag=True, help='Enable verbose mode.')
def my_cli(verbose):
    """Main CLI group."""
    pass

@my_cli.command()
@click.option('--name', prompt='Your name', help='The person to greet.')
@click.argument('times', type=int)
def greet(name, times):
    """Greet someone a number of times."""
    for _ in range(times):
        click.echo(f"Hello, {name}!")

@my_cli.group()
def math():
    """Math operations."""
    pass

@math.command()
@click.argument('x', type=int)
@click.argument('y', type=int)
def add(x, y):
    """Add two numbers."""
    click.echo(x + y)

@math.command()
@click.argument('x', type=int)
@click.argument('y', type=int)
def subtract(x, y):
    """Subtract two numbers."""
    click.echo(x - y)
```

```python
from click_summarizer import summarize_click_command
out = summarize_click_command(my_cli, show_help=True, show_options=True)
print(out.getvalue())
```

## License

`click-summarizer` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.

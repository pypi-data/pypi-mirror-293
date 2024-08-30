import click
import importlib
import sys

from .main import summarize_click_command

@click.command()
@click.argument('module_path')
@click.argument('cli_name')
@click.option('--no-doc', 'no_doc', is_flag=True, help='ignore docstrings.')
def summarize_cli(module_path, cli_name, no_doc):
    """Summarize a Click CLI app."""
    try:
        # Dynamically import the module
        module = importlib.import_module(module_path)

        # Get the CLI app from the module
        cli_app = getattr(module, cli_name)

        # Summarize the CLI app
        output_io = summarize_click_command(
            cli_app,
            show_help=not no_doc
        )

        print(output_io.getvalue())
        output_io.close()

    except (ImportError, AttributeError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    summarize_cli()

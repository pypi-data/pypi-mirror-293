from io import StringIO
from typing import Optional, TextIO
import click

def prepend_hash(lines, reformat_docstring=True):
    if reformat_docstring:
        lines = lines.strip().strip('#').strip()
    new_lines = []
    for line in lines.split('\n'):
        if line.strip():
            if line.strip().startswith('#'):
                new_lines.append(line)
            else:
                new_lines.append('# ' + line)
    return '\n'.join(new_lines)

def summarize_click_command(
        command: str,
        parent_name: str='',
        show_help: bool=True,
        show_options: bool=True,
        reformat_docstring: bool=True,
        output_io:Optional[TextIO]=None
    ) -> StringIO:
    # Build the command path

    if output_io is None:
        output_io = StringIO()

    command_path = f"{parent_name.strip()} {command.name}".strip()

    options_line = f"{command_path}"
    for param in command.params:
        if isinstance(param, click.Option):
            options_line += f" [--{param.name.replace('_', '-')}]"
        elif isinstance(param, click.Argument):
            options_line += f" [{param.name}]"

    should_print = True
    if isinstance(command, click.Group):
        should_print = False

    # Print the command help description
    help_line = f"# {command.help}"
    if should_print:    
        if show_help:
            output_io.write(prepend_hash(help_line, reformat_docstring=reformat_docstring) + '\n')
        if show_options:
            output_io.write(options_line + '\n')
        output_io.write('\n')  # Blank line for separation

    # Check if the command has subcommands
    if isinstance(command, click.Group):
        subcommand_options = ' '.join(
            f"[--{param.name.replace('_', '-')}]"
            for param in command.params if isinstance(param, click.Option)
        ).strip()

        for subcommand in command.commands.values():
            summarize_click_command(subcommand, command_path + ' ' +subcommand_options, show_help=show_help, show_options=show_options, output_io=output_io)
    return output_io
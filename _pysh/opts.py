import argparse
import os
from _pysh.shell import CONFIG_PREFIX
from _pysh.commands import install, download_deps, dist, activate, run, welcome


# The main argument parser.
parser = argparse.ArgumentParser(
    prog=os.environ["PYSH_SCRIPT_NAME"],
    description="Install and manage a standalone Python interpreter and dependencies.",
)

command_parsers = parser.add_subparsers(
    title="subcommands",
    help="The command to run.",
)

parser.add_argument(
    "--conda-env",
    default="app",
    help="The name of the conda environment to install the app into. Defaults to 'app'.",
)

parser.add_argument(
    "--environment-file",
    default="environment.yml",
    help="Path to a YAML dependencies file. Defaults to 'environment.yml' in the same directory as this script.",
)

parser.add_argument(
    "--shell",
    default="/bin/bash",
    help="The shell to use to run scripts in this environment. Defaults to '/bin/bash'.",
)

parser.add_argument(
    "--traceback",
    default=False,
    action="store_true",
    help="Enable tracebacks in errors.",
)

parser.set_defaults(**{
    key[len(CONFIG_PREFIX):].lower(): value
    for key, value
    in os.environ.items()
    if key.startswith(CONFIG_PREFIX)
})


# Install parser.

install_parser = command_parsers.add_parser(
    "install",
    help="Installs a standalone Python interpreter and all the app dependencies.",
)

install_parser.add_argument(
    "--offline",
    default=False,
    action="store_true",
    help=(
        "Install dependencies from an offline archive. This should only be run in an archive created using "
        "the 'dist' command, or after running the 'download-deps' command."
    ),
)

install_parser.set_defaults(func=install)


# Download deps command.

download_deps_parser = command_parsers.add_parser(
    "download-deps",
    help="Download dependencies required for install --offline.",
)

download_deps_parser.set_defaults(func=download_deps)


# Dist parser.

dist_parser = command_parsers.add_parser(
    "dist",
    help="Creates a standalone archive of this app and all it's dependencies.",
)

dist_parser.add_argument(
    "--output",
    default="dist/app.zip",
    help="The output filename. Defaults to 'dist/app.zip'.",
)

dist_parser.set_defaults(func=dist, conda_env="build")


# Activate command.

activate_parser = command_parsers.add_parser(
    "activate",
    help="Activates the standalone Python environment.",
)

activate_parser.set_defaults(func=activate)


# Run command.

run_parser = command_parsers.add_parser(
    "run",
    help="Runs shell command in the standalone Python environment.",
)

run_parser.set_defaults(func=run)


# Welcome command.

welcome_parser = command_parsers.add_parser(
    "welcome",
    help="Prints a cute welcome message.",
)

welcome_parser.set_defaults(func=welcome)


# Parses the options.

def parse_args(args):
    opts, unknown_args = parser.parse_known_args(args)
    opts.conda_lib_path = os.path.join(opts.lib_path, "conda")
    opts.pip_lib_path = os.path.join(opts.lib_path, "pip")
    return opts, unknown_args

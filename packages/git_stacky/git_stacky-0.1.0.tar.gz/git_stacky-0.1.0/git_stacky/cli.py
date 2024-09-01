#!/usr/bin/env python3

import subprocess
import sys
from enum import Enum
from pathlib import Path
from typing import Optional

import click

# Enable -h flag, rather than just --help
# REF: https://click.palletsprojects.com/en/7.x/documentation/#help-parameter-customization
CLICK_CTX_CONFIG = dict(
    help_option_names=["-h", "--help"],
)


class WorkflowType(Enum):
    BRANCH = "branch"
    FORK = "fork"


@click.group(context_settings=CLICK_CTX_CONFIG)
def cli():
    pass


@cli.command()
@click.argument("target", required=False)
# no update
@click.option("-n", "--no-update", is_flag=True, default=False, help="Do not update main.")
def hack(target: str, no_update: bool) -> None:
    """
    Update main and optionally create a new stack.

    \b
    Function:
      hack        => update main, stay on starting branch
      hack TARGET => update main, create TARGET from main if it doesn't exist, and switch to it

    \b
    Examples:
      (main)    hack          => update main
      (main)    hack FEATURE  => update main, create+switch to FEATURE
      (FEATURE) hack          => update main
      (FEATURE) hack main     => update main, switch to main
    """
    workflow = workflow_type()
    main_branch = main_branch_name()

    # Validate
    must_run("git status --porcelain", "current branch is dirty, aborting")
    start = current_branch()
    if not start and not target:
        log("start and target branches empty (detached head and no target), aborting")
        return
    validate_branches()
    create_target = validate_target_hack_branch(target, main_branch)

    # Update main
    if start != main_branch:
        must_run(f"git checkout {main_branch}")
    if not no_update:
        if workflow == WorkflowType.FORK:
            must_run(f"git pull upstream {main_branch}")
            must_run(f"git push origin {main_branch}")
        else:
            must_run("git pull")

    # Just updating main, so ensure ending on the starting branch
    if not target or target == main_branch:
        if start != main_branch:
            must_run(f"git checkout {start}")
        return

    # Create/switch to new stack
    if create_target:
        must_run(f"git branch {target}_base")
        must_run(f"git checkout -b {target}")
    else:
        must_run(f"git checkout {target}")


@cli.command()
@click.argument("target", required=False)
@click.option("-d", "--done", is_flag=True, default=False, help="Finish rebasing a stack.")
def rebase(target: str, done: bool) -> None:
    """
    Rebase current stack onto main or the specified target.

    \b
    Examples:
      (FEATURE) rebase        => rebase FEATURE onto main
      (FEATURE) rebase TARGET => rebase FEATURE onto TARGET
      (FEATURE) rebase --done => finish rebasing FEATURE, if original rebase was interrupted
    """
    if done:
        rebase_done()
        return

    rebase_only(target)
    rebase_done()


@cli.command()
@click.option("-g", "--graph", is_flag=True, default=False, help="Print a graph of all stacks.")
@click.option("-d", "--delete", multiple=True, help="Delete a stack.")
@click.option("-D", "--delete-force", multiple=True, help="Delete a stack forcefully.")
def stacks(graph: bool, delete: tuple[str], delete_force: tuple[str]) -> None:
    """
    Manage and visualize stacks.

    \b
    Examples:
      stacks                     => list all stacks
      stacks --graph             => graph all stacks
      stacks --delete FEATURE    => delete FEATURE stack
    """
    if delete or delete_force:
        if delete:
            delete_stacks(list(delete))
        if delete_force:
            delete_stacks(list(delete_force), force=True)
        return
    if graph:
        subprocess.run(
            [
                "git",
                "log",
                "--graph",
                "--format=format:%C(auto)%h%C(reset) %C(cyan)(%cr)%C(reset)%C(auto)%d%C(reset) %s %C(dim white)- %an%C(reset)",
            ]
            + get_stacks(),
        )
        return
    list_stacks()


@cli.command()
def absorb() -> None:
    """
    Automatically absorb changes into the stack.

    Requires git-absorb to be installed.
    """
    if not try_run("git absorb -h"):
        cexit("ERROR: git-absorb not installed, aborting")
    current = current_branch()
    if not current:
        log("current branch not found (detached head), aborting")
        return
    if current not in get_stacks():
        log("current branch is not a stack, aborting")
        return
    subprocess.run(
        [
            "git",
            "-c",
            "sequence.editor=:",
            "-c",
            "absorb.autoStageIfNothingStaged=true",
            "absorb",
            "--and-rebase",
            "--base",
            f"{current}_base",
        ]
    )


def rebase_only(target: str) -> None:
    """Rebase a stack onto the target."""
    br = must_run("git branch --show-current", "current branch not found, aborting")
    br_base = f"{br}_base"

    if not branch_exists(br):
        cexit(f"current branch '{br}' does not exist, aborting")
    if not branch_exists(br_base):
        cexit(f"stack may not be tracked by stacky: base branch '{br_base}' does not exist, aborting")
    if target and not branch_exists(target):
        log(f"target branch '{target}' does not exist, aborting")
    if not target:
        target = main_branch_name()
    if target == br:
        cexit("target branch is the same as current branch, aborting")
    if target == br_base:
        cexit("target branch is the same as base branch, aborting")

    save_rebase_args([target, br_base, br])

    res = subprocess.run(["git", "rebase", "--onto", target, br_base, br], text=True, capture_output=True)
    if res.returncode:
        click.echo("WARNING: rebase failed")
        click.echo("RUN: 'git stack rebase --done' to complete rebase, after resolving conflicts")
        click.echo()
        click.echo(res.stderr)
        exit(1)


def rebase_done() -> None:
    """Finish rebasing a stack."""
    args = load_rebase_args()
    if len(args) != 3:
        log("rebase arguments not found, aborting")
        return
    target, br_base, br = args

    if not branch_exists(br):
        log(f"branch '{br}' does not exist, aborting")
        return
    if not branch_exists(br_base):
        log(f"base branch '{br_base}' does not exist, aborting")
        return

    must_run(f"git checkout {br_base}")
    must_run(f"git reset --hard {target}")
    must_run(f"git checkout {br}")

    clear_rebase_args()


def save_rebase_args(args: list[str]) -> None:
    """Save null-separated rebase arguments to ~/.stacky/rebase_args."""
    stacky_dir = Path.home() / ".stacky"
    rebase_args_file = stacky_dir / "rebase_args"
    stacky_dir.mkdir(parents=True, exist_ok=True)
    rebase_args_file.write_text("\0".join(args))


def load_rebase_args() -> list[str]:
    """Load null-separated rebase arguments from ~/.stacky/rebase_args."""
    rebase_args_file = Path.home() / ".stacky" / "rebase_args"
    if not rebase_args_file.exists():
        return []
    return rebase_args_file.read_text().split("\0")


def clear_rebase_args() -> None:
    """Clear rebase arguments."""
    rebase_args_file = Path.home() / ".stacky" / "rebase_args"
    if rebase_args_file.exists():
        rebase_args_file.unlink()


def delete_stacks_all(force: bool = False) -> None:
    """Delete all stacks."""
    stacks = get_stacks()
    stacks = [s for s in stacks if s if not s == current_branch()]
    delete_stacks(stacks, force)


def delete_stacks(delete: list[str], force: bool = False) -> None:
    """Delete stacks."""
    delete = set(delete).intersection(get_stacks())
    delete = [s for s in delete] + [f"{s}_base" for s in delete]
    if not delete:
        log("no stacks to delete")
        return

    res = subprocess.run(["git", "branch", "-D" if force else "-d"] + list(delete), text=True, capture_output=True)
    if res.returncode:
        log("ERROR: delete failed")
        click.echo()
        click.echo(res.stderr)
        return


def list_stacks() -> None:
    """List all tracked stacks."""
    stacks = [f"* {s}" if s == current_branch() else f"  {s}" for s in get_stacks()]
    if not stacks:
        return
    click.echo("\n".join(stacks))


def get_stacks() -> list[str]:
    """Return a list of tracked stacks."""
    branches = get_branches()
    stacks = [b for b in branches if f"{b}_base" in branches]
    return stacks


def get_branches() -> list[str]:
    """Return a list of branches."""
    return must_run("git branch --format='%(refname:short)'").split()


def main_branch_name() -> str:
    """Return the name of the main branch."""
    name = try_run("git symbolic-ref refs/remotes/origin/HEAD")
    if name:
        return name.split("/")[-1]

    name = try_run("git config --get init.defaultBranch")
    if name:
        return name

    return "master"


def workflow_type() -> WorkflowType:
    """Return the type of Git workflow."""
    if try_run("git remote get-url upstream"):
        return WorkflowType.FORK
    return WorkflowType.BRANCH


def branch_exists(target: str) -> bool:
    """Check if a branch exists."""
    return bool(try_run(f"git show-ref refs/heads/{target}"))


def current_branch() -> str:
    """Return the name of the current branch, or an empty string if detached."""
    return try_run("git branch --show-current")


def validate_branches(target: str = "") -> None:
    """Validate branch names."""
    branches = get_branches()
    stacks = get_stacks()
    for b in branches:
        if b.endswith("_base_base"):
            log(f"WARNING: potentially colliding base branch '{b}' detected")
        if b.endswith("_base") and strip_suffix(b, "_base") not in stacks:
            log(f"WARNING: potentially orphaned base branch '{b}' detected")


def validate_target_hack_branch(target: str, main_branch: str) -> bool:
    """Validate the target branch for the hack command. Returns True iff the target needs to be created."""
    if not target or target == main_branch:
        return False

    target_exists = branch_exists(target)
    target_base_exists = branch_exists(f"{target}_base")
    if target_exists and not target_base_exists:
        cexit(f"ERROR: target branch '{target}' exists, but base branch '{target}_base' does not, aborting")
    if not target_exists and target_base_exists:
        cexit(f"ERROR: base branch '{target}_base' exists, but target branch '{target}' does not, aborting")
    if target_exists and target_base_exists:
        log(f"WARNING: stack '{target}' already exists")
        return False
    return True


def strip_suffix(s: str, suffix: str) -> str:
    """Strip a suffix from a string."""
    if s.endswith(suffix):
        return s[: -len(suffix)]
    return s


def run(command: str) -> tuple[str, str, int]:
    """Run a shell command and return the output."""
    res = subprocess.run(command, shell=True, text=True, capture_output=True)
    return res.stdout.strip(), res.stderr.strip(), res.returncode


def must_run(command: str, fail_msg: Optional[str] = None) -> str:
    """Run a shell command and return the output, or exit on error."""
    out, err, errcode = run(command)
    if errcode:
        msg = fail_msg or f"ERROR: failed to run command ({errcode}): {command}\n\n{err}"
        cexit(msg)
    return out


def try_run(command: str) -> Optional[str]:
    """Run a shell command and return the output, or return None on error."""
    out, _, errcode = run(command)
    if errcode:
        return ""
    return out


def cexit(msg: str) -> None:
    """Print an error message and exit."""
    log(msg)
    sys.exit(1)


def log(msg: str) -> None:
    """Print a message."""
    click.echo(fmt_log(msg))


def fmt_log(msg: str) -> str:
    """Capitalize the first letter of a log message."""
    if not msg:
        return msg
    return msg[0].upper() + msg[1:]


if __name__ == "__main__":
    cli()

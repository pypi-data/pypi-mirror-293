"""
 
 This module use twine for publishing packages.
 
"""

from invoke import run
from invoke import task


@task
def clean(ctxt):
    """
    Clean build directory.
    """
    run("rm dist/*")


@task(name="build")
def build_tsk(ctxt):
    """
    Build package for publishing to PyPI
    """
    run("python3 -m build")


@task
def publish(ctxt, repository):
    """
    Publish package and push to all remotes: --repository <>
    
    The mandtory `--repository` option expects repositories to be configured in `~/.pypirc`.
    """
    run(f"twine upload --repository {repository} dist/*")
    run("git remote | xargs -I remote git push remote")

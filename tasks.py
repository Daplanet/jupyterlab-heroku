"""
Sideloader buildpack init - v1.0
"""

import os
from pathlib import Path
from invoke import task, call

EXTS = [
    { "name": "jupyter_dashboards", "type": 0 },
    { "name": "jupyterlab", "type": 1 },
    { "name": "voila", "type": 1 },
    { "name": "@voila-dashboards/jupyterlab-preview", "type": 2 }]

EXT_TYPE_ENUM = [ "nb", "server", "lab" ]

@task
def setup(ctx, props):
    """ Installs and configures environment post buildpack """
    props['root'].mkdir()

    for ext in props['extentions']:
        ctx.run(f"jupyter {EXT_TYPE_ENUM[ext.type]}extention install --py {ext.name} --sys-prefix")
        ctx.run(f"jupyter {EXT_TYPE_ENUM[ext.type]}extention enable --py {ext.name} --sys-prefix")

        if ext.type == int(2):
            ctx.run(f"jupyter {EXT_TYPE_ENUM[ext.type]}extention install {ext.name}")

@task(default=True)
def launch(ctx):
    """ Serves web.1 dyno with shell script """
    ctx.run("./launch.sh")

@task
def serve(ctx):
    """ Serves web.1 dyno. """
    root = Path("./root")

    if not root.is_dir():
        call(setup, props={ "root": root, "extentions": EXTS })

    with ctx.cd(str(root)):
        with ctx.prefix("export JUPYTER_CONFIG_DIR=/app"):
            ctx.run(f"jupyter lab --port={os.environ.get('PORT', 3000)}")

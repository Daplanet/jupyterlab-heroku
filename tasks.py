import os
from pathlib import Path
from invoke import task, call

EXT_TYPE_ENUM = [
  "nb",
  "server",
  "lab"
]

@task
def setup(ctx, props={}):
  props['root'].mkdir()

  for ext in props['extentions']:
    ctx.run(f"jupyter {EXT_TYPE_ENUM[ext.type]}extention install --py {ext.name} --sys-prefix")
    ctx.run(f"jupyter {EXT_TYPE_ENUM[ext.type]}extention enable --py {ext.name} --sys-prefix")

    if ext.type is 2:
      ctx.run(f"jupyter {extention_type_enum[ext.type]}extention install {ext.name}")      

@task(default=True)
def serve(ctx):
  root = Path("./root")
  exts = [
    { name: "jupyter_dashboards", type: 0 },
    { name: "jupyterlab", type: 1 },
    { name: "voila", type: 1 },
    { name: "@voila-dashboards/jupyterlab-preview", type: 2 }]

  if not root.is_dir():
    call(setup, { root: root, extentions = exts })

  with ctx.cd(str(root)):
    with ctx.prefix("export JUPYTER_CONFIG_DIR=/app"):
      ctx.run(f"jupyter lab --port={os.environ.get('PORT', 3000)}")

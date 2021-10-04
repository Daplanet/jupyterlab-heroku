import os
from pathlib import Path
from invoke import exception, task, call

extention_type_enum = [
  "nb",
  "server",
  "lab"
]

extentions = [
  { name: "jupyter_dashboards", type: 0 },
  { name: "jupyterlab", type: 1 },
  { name: "voila", type 1 },
  { name: "@voila-dashboards/jupyterlab-preview", type: 2 }
]

root = Path("./root")

@task
def setup(ctx):
  root.mkdir()

  for ext in extentions:
    ctx.run(f"jupyter {extention_type_enum[ext.type]}extention install --py {ext.name} --sys-prefix")
    ctx.run(f"jupyter {extention_type_enum[ext.type]}extention enable --py {ext.name} --sys-prefix")

    if ext.type is 2:
      ctx.run(f"jupyter {extention_type_enum[ext.type]}extention install {ext.name}")      

@task(default=True)
def serve(ctx):
  if not root.is_dir():
    call(setup)

  with ctx.cd(str(root)):
    with ctx.prefix("export JUPYTER_CONFIG_DIR=/app"):
      ctx.run(f"jupyter lab --port={os.environ.get('PORT', 3000)}")

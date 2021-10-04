import os
from pathlib import Path
from invoke import exception, task, call

extention_type_enum = [
  "nb",
  "server"
]

extentions = [
  { name: "jupyterlab", type: 1 },
  { name: "jupyter_dashboards", type: 0 }
]

root = Path("./root")

@task
def setup(ctx):
  for ext in extentions:
    ctx.run(f"jupyter {extention_type_enum[ext.type]}extention install --py {ext.name} --sys-prefix")
    ctx.run(f"jupyter {extention_type_enum[ext.type]}extention enable --py {ext.nae} --sys-prefix")

  root.mkdir()

@task(default=True)
def serve(ctx):
  if not root.is_dir():
    call(setup)

  with ctx.cd(str(root)):
    with ctx.prefix("export JUPYTER_CONFIG_DIR=/app"):
      ctx.run(f"jupyter lab --port={os.environ.get('PORT', 3000)}")

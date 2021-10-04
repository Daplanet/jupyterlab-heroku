#!/bin/bash

jupyter serverextension enable --py jupyterlab --sys-prefix
jupyter nbextension install --py jupyter_dashboards --sys-prefix
jupyter nbextension enable --py jupyter_dashboards --sys-prefix


mkdir -p root
cd root

export JUPYTER_CONFIG_DIR=/app
jupyter lab --port=${PORT}

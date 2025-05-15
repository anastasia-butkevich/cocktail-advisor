#!/bin/bash

uvicorn app.api.routes:app --host 0.0.0.0 --port 8000 &

streamlit run app/ui/streamlit_ui.py --server.port 8501 --server.address 0.0.0.0

wait -n

exit $?
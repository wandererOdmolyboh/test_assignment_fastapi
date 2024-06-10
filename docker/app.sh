#!/bin/bash

alembic upgrade head
python tests/fill_test_data.py

gunicorn src.main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
#!/bin/bash
# Stop the server
kill $(ps aux | grep 'uvicorn img_api:app' | awk '{print $2}')
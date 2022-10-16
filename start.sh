#!/bin/bash
# Start the server
nohup uvicorn img_api:app --reload > log.txt &
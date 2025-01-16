#!/bin/bash

tail -f autodeploy.log frontend/logs/$(ls -t frontend/logs/|head -1) backend/logs/$(ls -t backend/logs/|head -1)


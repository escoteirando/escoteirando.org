#!/bin/bash

echo "Running unit tests..."
coverage run -m unittest unit_tests.py
echo "Generating coverage..."
coverage xml
echo "Done"
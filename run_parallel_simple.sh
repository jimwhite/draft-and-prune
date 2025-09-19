#!/bin/bash

# Simple script to run all experiments in parallel background
echo "Starting 4 parallel experiments..."

# Create timestamp for log directory
TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)
LOG_DIR="./logs/parallel_$TIMESTAMP"
mkdir -p "$LOG_DIR"

# Run all experiments in background
python3 main.py config_gpt4_2-CoT-align.yaml > "$LOG_DIR/gpt4_2-CoT-align.log" 2>&1 &
echo "Started GPT-4 2-CoT-align (PID: $!)"

python3 main.py config_gpt4o_2-CoT-align.yaml > "$LOG_DIR/gpt4o_2-CoT-align.log" 2>&1 &
echo "Started GPT-4o 2-CoT-align (PID: $!)"

python3 main.py config_gpt4_3-sketch-align.yaml > "$LOG_DIR/gpt4_3-sketch-align.log" 2>&1 &
echo "Started GPT-4 3-Sketch-align (PID: $!)"

python3 main.py config_gpt4o_3-sketch-align.yaml > "$LOG_DIR/gpt4o_3-sketch-align.log" 2>&1 &
echo "Started GPT-4o 3-Sketch-align (PID: $!)"

echo ""
echo "All experiments started in background!"
echo "Logs will be saved to: $LOG_DIR/"
echo ""
echo "To monitor:"
echo "  tail -f $LOG_DIR/*.log"
echo "  ps aux | grep main.py"
echo "  jobs"

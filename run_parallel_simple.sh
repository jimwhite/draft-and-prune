#!/bin/bash

# Simple script to run all experiments in parallel background
echo "Starting parallel experiments..."

# Create timestamp for log directory
TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)
LOG_DIR="./logs/parallel_$TIMESTAMP"
mkdir -p "$LOG_DIR"

# Run all experiments in background
# python3 main.py config_gpt4_2-CoT-align.yaml > "$LOG_DIR/gpt4_2-CoT-align.log" 2>&1 &
# echo "Started GPT-4 2-CoT-align (PID: $!)"

# python3 main.py config_gpt4o_2-CoT-align.yaml > "$LOG_DIR/gpt4o_2-CoT-align.log" 2>&1 &
# echo "Started GPT-4o 2-CoT-align (PID: $!)"

# python3 main.py config_gpt4_3-sketch-align.yaml > "$LOG_DIR/gpt4_3-sketch-align.log" 2>&1 &
# echo "Started GPT-4 3-Sketch-align (PID: $!)"

# python3 main.py config_gpt4o_3-sketch-align.yaml > "$LOG_DIR/gpt4o_3-sketch-align.log" 2>&1 &
# echo "Started GPT-4o 3-Sketch-align (PID: $!)"

# python3 main.py config_gemini_2dot5_pro_3_shot_cot.yaml > "$LOG_DIR/gemini_2dot5_pro_3_shot_cot.log" 2>&1 &
# echo "Started Gemini 2.5 Pro 3-Shot CoT (PID: $!)"

# python3 main.py config_gemini_2dot5_flash_3_shot_cot.yaml > "$LOG_DIR/gemini_2dot5_flash_3_shot_cot.log" 2>&1 &
# echo "Started Gemini 2.5 Flash 3-Shot CoT (PID: $!)"

# GPT-4 3-Shot CoT
# python main.py config_gpt4_3_shot_cot.yaml > "$LOG_DIR/gpt4_3_shot_cot.log" 2>&1 &
# echo "Started GPT-4 3-Shot CoT (PID: $!)"

# # GPT-4 One-Step
# python main.py config_ar-lsat_gpt4_one-step.yaml > "$LOG_DIR/ar-lsat_gpt4_one-step.log" 2>&1 &
# echo "Started AR-LSAT GPT-4 One-Step (PID: $!)"

python main.py config_gemini_proofwriter_usc.yaml > "$LOG_DIR/gemini_proofwriter_usc.log" 2>&1 &
echo "Started Gemini ProofWriter USC (PID: $!)"

# GPT-4 Sketch Only
# python main.py config_ar-lsat_gpt4_sketch_only.yaml > "$LOG_DIR/ar-lsat_gpt4_sketch_only.log" 2>&1 &
# echo "Started AR-LSAT GPT-4 Sketch Only (PID: $!)"

echo ""
echo "All experiments started in background!"
echo "Logs will be saved to: $LOG_DIR/"
echo ""
echo "To monitor:"
echo "  tail -f $LOG_DIR/*.log"
echo "  ps aux | grep main.py"
echo "  jobs"

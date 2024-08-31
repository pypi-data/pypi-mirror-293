import os

# Setup
SEED_NUM = 42
NUM_WORKERS = os.cpu_count() or 0

# Training arguments
NUM_EPOCHS = 10
BATCH_SIZE = 16
LEARNING_RATE = 0.001

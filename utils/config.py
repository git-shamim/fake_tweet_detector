# Flag to control whether to use a fine-tuned model
USE_FINETUNED_MODEL = False

# Path to fine-tuned model when USE_FINETUNED_MODEL is True
# This should match the mount point in Cloud Run when you add blob storage
MODEL_PATH = "/mnt/models/bertweet_finetuned"

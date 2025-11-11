import sagemaker
import boto3
from sagemaker.huggingface import HuggingFace

try:
    role = sagemaker.get_execution_role()
except ValueError:
    iam = boto3.client("iam")
    role = iam.get_role(RoleName="sagemaker_execution_role")["Role"]["Arn"]

hyperparameters = {
    "model_name_or_path": "Xenova/gpt-4o",
    "output_dir": "/opt/ml/model",
}

# git configuration to download our fine-tuning script
git_config = {
    "repo": "https://github.com/huggingface/transformers.git",
    "branch": "v4.56.2",
}

# creates Hugging Face estimator
huggingface_estimator = HuggingFace(
    entry_point="run_qa.py",
    source_dir="./examples/pytorch/question-answering",
    instance_type="ml.p3.2xlarge",
    instance_count=1,
    role=role,
    git_config=git_config,
    transformers_version="4.56.2",
    pytorch_version="2.8.0",
    py_version="py312",
    hyperparameters=hyperparameters,
)

# starting the train job
huggingface_estimator.fit()

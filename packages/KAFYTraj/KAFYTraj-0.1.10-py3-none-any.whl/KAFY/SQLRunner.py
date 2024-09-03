import re
from KAFY.Pipeline import *


def pretrain_model(data_path, config_path, output_name):
    # Initialize and run your pretraining pipeline here
    pipeline = TrajectoryPipeline(
        mode="pretraining",
        operation_type="generation",
        use_tokenization=True,
        use_detokenization=True,
        use_spatial_constraints=True,
        modify_spatial_constraints=True,
        use_predefined_spatial_constraints=True,
        project_path="/content",
    )
    # Pretrain logic
    print(f"Pretrained model saved as {output_name}", pipeline)


def finetune_model(task, pretrained_model_path, config_path, output_name):
    # Initialize and run your fine-tuning pipeline here
    pipeline = TrajectoryPipeline(
        mode="finetuning",
        operation_type=task,
        # other relevant configurations
    )
    # Fine-tuning logic
    print(f"Fine-tuned model saved as {output_name}")


def summarize_data(data_path, model_path):
    # Initialize and run your summarization pipeline here
    pipeline = TrajectoryPipeline(
        mode="operation",
        operation_type="summarization",
        # other relevant configurations
    )
    # Summarization logic
    print("Summarization complete")


def parse_command(command=None):
    if command is None:
        command = " ".join(
            sys.argv[1:]
        )  # Join command-line arguments into a single string

    # The rest of your parsing logic remains the same

    pretrain_match = re.match(
        r"PRETRAIN\s+(\w+)\s+FROM\s+(\S+)\s+USING\s+(\S+)\s+AS\s+(\S+)",
        command,
        re.IGNORECASE,
    )
    finetune_match = re.match(
        r"FINETUNE\s+(\w+)\s+FOR\s+(\w+)\s+USING\s+(\S+)\s+WITH\s+(\S+)\s+AS\s+(\S+)",
        command,
        re.IGNORECASE,
    )
    summarize_match = re.match(
        r"SUMMARIZE\s+FROM\s+(\S+)\s+USING\s+(\S+)", command, re.IGNORECASE
    )

    if pretrain_match:
        model, data, config, output_name = pretrain_match.groups()
        pretrain_model(data, config, output_name)
    elif finetune_match:
        model, task, pretrained_model, config, output_name = finetune_match.groups()
        finetune_model(task, pretrained_model, config, output_name)
    elif summarize_match:
        data, model = summarize_match.groups()
        summarize_data(data, model)
    else:
        print("Command not recognized.")

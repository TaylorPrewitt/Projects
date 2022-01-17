# import packages
import argparse
from azureml.core.authentication import InteractiveLoginAuthentication
from azureml.core import Workspace, Environment, Experiment, Dataset, ScriptRunConfig

if __name__ == '__main__':
    # read in arguments to run the azure pipeline
    # - this is just copied from `train.py` and passes along the inputs
    parser = argparse.ArgumentParser(
        description='RUN Baseline model of MedMNIST')
    parser.add_argument('--data_name',
                        default='pathmnist',
                        help='subset of MedMNIST',
                        type=str)
    parser.add_argument('--input_root',
                        default='./input',
                        help='input root, the source of dataset files',
                        type=str)
    parser.add_argument('--output_root',
                        default='./output',
                        help='output root, where to save models and results',
                        type=str)
    parser.add_argument('--num_epoch',
                        default=100,
                        help='num of epochs of training',
                        type=int)
    parser.add_argument('--download',
                        default=True,
                        help='whether download the dataset or not',
                        type=bool)
    parser.add_argument('--model_name',
                        default='ResNet18',
                        help='which model to use',
                        type=str)
    args = parser.parse_args()

    # set up workspace
    config_path = 'utils/config.json'
    tenant_id = '72f988bf-86f1-41af-91ab-2d7cd011db47'  # this is outputted post `az login`
    interactive_auth = InteractiveLoginAuthentication(tenant_id=tenant_id)  # create log-in object
    ws = Workspace.from_config(path=config_path, auth=interactive_auth)  # link workspace

    # set up environment
    env_name = 'ImageProcessing'
    env_path = 'utils/environment.yml'
    env = Environment.from_conda_specification(name=env_name, file_path=env_path)
    # - set docker from curate environment
    env.docker.enabled = True
    env.docker.base_image = 'mcr.microsoft.com/azureml/openmpi4.1.0-cuda11.1-cudnn8-ubuntu18.04'

    # set up experiment
    experiment_name = 'ImageProcessing'
    exp = Experiment(workspace=ws, name=experiment_name)

    # set up run
    src_dir = '.'
    src_name = 'train.py'
    compute_name = 'gpu-compute-one'
    arguments = ['--data_name', args.data_name, '--input_root', args.input_root, '--output_root', args.output_root, '--num_epoch', args.num_epoch, '--download', args.download, '--model_name', args.model_name]
    print(arguments)
    src = ScriptRunConfig(source_directory=src_dir, script=src_name, compute_target=compute_name,
                          environment=env, arguments=arguments)

    # submit run
    run = exp.submit(src)  # submit it to the azureml platform
    run.wait_for_completion(show_output=True)

import os

from .oss import OSS
from .ckpt import Ckpt
from .wrapper import timeit


@timeit
def fetch_checkpoint(model_path, local_dir, example_command, verbose=False, skip_download=False):
    if not skip_download:
        # download checkpoint from oss
        if model_path.endswith('all'):
            model_path = model_path + '/'
        if not model_path.endswith('all/'):
            raise NameError('model_path should end with "all/"')

        oss = OSS(example_command, verbose=verbose)

        model_list = oss.list_model(model_path)
        max_step = max(model_list).split('-')[-1]  # '308928299'
        model_files = oss.list_dir(model_path, filter_fn=lambda s: f'model.ckpt-{max_step}.' in s)

        if verbose:
            print(f'files to be download = {model_files}')

        os.system(f'rm -r {local_dir}')
        os.makedirs(local_dir, exist_ok=True)

        if verbose:
            print("download models")
        for file in model_files:
            oss.download(file, local_dir, is_dir=False)
    else:
        print(f'skip download! use checkpoint from {local_dir}')

    local_model_files = os.listdir(local_dir)
    if verbose:
        print(f"local_model_files = {local_model_files}")

    ckpt_name = '.'.join(local_model_files[0].split('.')[:2])
    ckpt_path = os.path.join(local_dir, ckpt_name)
    ckpt = Ckpt(ckpt_path)
    return ckpt



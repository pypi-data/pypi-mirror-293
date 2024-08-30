import tensorflow as tf
import numpy as np
import warnings

warnings.filterwarnings('ignore')


class Ckpt:
    def __init__(self, path):
        self.ckpt_reader = tf.train.load_checkpoint(path)
        self.var_map = {name: shape for name, shape in tf.train.list_variables(path)}  # {var_name: var_shape}

    def get(self, name):
        return self.ckpt_reader.get_tensor(name)

    def list_var(self, fn_dict=None, sep=', ', adam=False, filter_fn=None):
        tensor_dict = self.var_map if adam else {k: v for k, v in self.var_map.items() if ('Adam' not in k)}
        if filter_fn is not None:
            tensor_dict = {k: v for k, v in tensor_dict.items() if filter_fn(k)}

        for k, v in tensor_dict.items():
            tensor = self.get(k)
            info_list = [f'[{k}]: {v}']
            if (fn_dict is not None) and len(fn_dict) > 0:
                for name, fn in fn_dict.items():
                    info_list.append(f'{name} = {fn(tensor)}')
            if sep == '\n':
                info_list.append('\n')  # single '\n' to split fields, double '\n' to split tensors
            print(sep.join(info_list))

    def summary(self, names=None, adam=False, quantiles=None):
        if names is None:
            name_list = list(self.var_map.keys())
        elif type(names) == str:
            name_list = [names]
        elif type(names) == list:
            name_list = names
        else:
            raise NotImplementedError(f"type(names) = {type(names)}")

        if not adam:
            name_list = [name for name in name_list if ('Adam' not in name)]
        info_list = [self.summary_single(name, quantiles=quantiles) for name in name_list]
        info = '\n\n'.join(info_list)
        print(info)

    def summary_single(self, name, quantiles=None):
        tensor = self.get(name)
        info = [f'[{name}]', f'shape = {tensor.shape}', f'param_num = {np.prod(tensor.shape)}']

        if np.prod(np.prod(tensor.shape) <= 10):
            info.append(f'value = {tensor}')
        else:
            if quantiles is None:
                quantiles = [0, 0.25, 0.5, 0.75, 1]
            quantile_dict = {q: np.quantile(tensor, q) for q in quantiles}
            info.append(f"quantiles = {quantile_dict}")
        return '\n'.join(info)

    def get_param_num(self, filter_fn=None):
        tensor_dict = self.var_map
        if filter_fn is not None:
            tensor_dict = {k: v for k, v in tensor_dict.items() if filter_fn(k)}
        num = sum([np.prod(shape) for shape in tensor_dict.values()])
        if num < 1024:
            print(f"param_num = %i" % num)
        elif num < 1024 ** 2:
            print(f"param_num = %.2fK" % (num / 1024))
        elif num < 1024 ** 3:
            print(f"param_num = %.2fM" % (num / 1024 / 1024))
        return num


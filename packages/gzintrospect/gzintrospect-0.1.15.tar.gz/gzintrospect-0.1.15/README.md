# 使用
```python
# pip install gzintrospect
from gzintrospect import fetch_checkpoint
 
# 申请地址: https://quotacenter.devops.sit.xiaohongshu.com/algo/AlgoApplySTS
# 将申请的command example粘贴到下面即可
example_command = """
ossutilmac64 -t CAIS2gJ1q6Ft5B2yfSjIr5fzDP6Gle5A5KWSdhLhsXAkVtZd2byZrzz2IHhLf3JvBusXtv42mmpR5/kflrNoS5JDV0zDcNttxoRW+AShZIzOoMyoq7cDjcUfusV19kSpsvXJasDVEfn/GJ70GX2m+wZ3xbzlD0bAO3WuLZyOj7N+c90TRXPWRDFaBdBQVGAAwY1gQhm3D/u2NQPwiWf9FVdhvhEG6Vly8qOi2MaRmHG85R/YsrZK992sfcT6MZA0ZckmDIyPsbYoJvab4kl58ANX8ap6tqtA9Arcs8uVa1sruE3ZaLGLrYY+dFUgOPJjSvEZtoT7m/N8u+re0pjtwhdLPOdaFjjaXJAlPB1KogFUXTxQV8EYWxylurjnXvF+Y7+a+mX5zXtVYSwnM1F6Pw4CQP8mRsBcAKgzs85KpnlIKWjvGFe4PpQFLCPgzCLsPF7hOk1DUobWk1J2X3Z+GoABPW7q9rmfTe3+z7ped5iMA0TS1JqsMTkwjkbQRG2/4g0hVXwerEEGurJ0s2QDJQVbCqA6icOKqyZwB0f2tkH+XLB9RWWsGcLUSvHwH7ZvZVPjVLMVm9hLX9etVBqfGk4sfEYHVWo6qt0oYnhJeKPRWHED6XPE21GDZZurNv/gmX0gAA== -i STS.NTFGD2x1aSgyt4PUpqZYq6y2M -k Cf23RTTMzhW5C9L8eUG9QkLMW1G7FTFiQfmRQB6WpjAc ls oss://offline-training-persistent/ -d
"""  
 
model_path = 'oss://offline-training-model/larc_plat/model/homefeed_recall/recall_dssm_newneg_ali_imp/train/2024-08-11/x2a_Larc_Training/all/'
local_dir = './my_ckpt'
 
ckpt = fetch_checkpoint(model_path, local_dir, example_command, verbose=False)  # about 45s
ckpt.var_map
 
# ckpt.get('models/note_tower_1_dnn_model/dnn_layer_1/BatchNorm/moving_mean')
```

# 开发
发版： 修改setup.py中的版本号（+1），运行`sh publish.sh`

**打包**：
使用`setuptools`打包你的包：

```bash
python setup.py sdist bdist_wheel
```

**安装包**：
你可以使用`pip`安装你的包，以进行测试：

```bash
pip install .
```

**分发包**：
当你准备将包分发给其他人时，你可以将其上传到PyPI：

```bash
# pip install twine
twine upload dist/*
```

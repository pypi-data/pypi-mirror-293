import os
import re


class OSS:
    def __init__(self, example_command=None, replace_s3=False, verbose=False):
        """
        :param example_command: 申请地址: https://quotacenter.devops.sit.xiaohongshu.com/algo/AlgoApplySTS
        :param replace_s3: 是否将 s3:// 替换为 oss://
        :param verbose: 会否打印log
        """

        self.token = None
        self.ak = None   # AccessKeyId, e.g. "STS.NV4gtJLjZSKrUFXVGuDv1VnGB"
        self.sk = None   # AccessKeySecret, e.g. "7b3eeVwHmHfeicZEZey4DhYwweiKvrsfpwHYThVLGPXP"
        self.cmd_prefix = None

        if example_command is not None:
            self.parse(example_command)

        self.replace_s3 = replace_s3
        self.verbose = verbose

    def info(self, s):
        if self.verbose:
            print(s)

    def run(self, cmd):
        cmd = f'{self.cmd_prefix} {cmd}'
        res = []
        with os.popen(cmd) as fr:
            for line in fr:
                line = line.strip()
                res.append(line)
        return res

    def parse(self, example_command):
        parts = example_command.strip().split()
        for k, v in zip(parts[:-1], parts[1:]):
            if k == '-t':
                self.token = v
            if k == '-i':
                self.ak = v
            if k == '-k':
                self.sk = v
        self.cmd_prefix = f"ossutilmac64 -t {self.token} -i {self.ak} -k {self.sk} "

    def ls(self, path, filter_fn=None):
        if self.replace_s3:
            path = path.replace('s3://', 'oss://')
        cmd = f'{self.cmd_prefix} ls {path} -s'
        self.info(cmd)

        res = []
        with os.popen(cmd, 'r') as fr:
            for line in fr:
                line = line.strip()
                if not line.startswith("oss://"):
                    continue
                if (filter_fn is not None) and not filter_fn(line):
                    continue
                res.append(line)
        return res

    def list_dir(self, path, filter_fn=None):
        if self.replace_s3:
            path = path.replace('s3://', 'oss://')
        cmd = f'{self.cmd_prefix} ls {path} -d'
        self.info(cmd)

        res = []
        with os.popen(cmd, 'r') as fr:
            for line in fr:
                line = line.strip()
                if (filter_fn is not None) and not filter_fn(line):
                    continue
                res.append(line)
        return res

    def list_model(self, path):
        if self.replace_s3:
            path = path.replace('s3://', 'oss://')
        cmd = f'{self.cmd_prefix} ls {path} -d'
        self.info(cmd)

        res = []
        with os.popen(cmd, 'r') as fr:
            for line in fr:
                if len(line) < 30:
                    continue
                model = re.search("(model.ckpt-\d+)", line)
                if model:
                    res.append(os.path.join(path, model.groups()[0]))
        res = list(set(res))
        res = sorted(res)
        return res

    def copy(self, src, dest, is_dir=False):
        if self.replace_s3:
            src = src.replace('s3://', 'oss://')
            dest = dest.replace('s3://', 'oss://')
        cmd = f"{self.cmd_prefix} cp {'-r' if is_dir else ''} {src} {dest}"
        self.info(cmd)

        res = []
        with os.popen(cmd, 'r') as fr:
            for line in fr:
                line = line.strip()
                res.append(line)
        return res

    def upload(self, src, dest, is_dir=False):
        if self.replace_s3:
            dest = dest.replace('s3://', 'oss://')
        cmd = f"{self.cmd_prefix} cp {'-r' if is_dir else ''} {src} {dest}"
        self.info(cmd)
        res = []

        with os.popen(cmd, 'r') as fr:
            for line in fr:
                line = line.strip()
                res.append(line)
        return res

    def download(self, src, dest, is_dir=True, filter_fn=None, max_num=None):
        if self.replace_s3:
            src = src.replace('s3://', 'oss://')

        if filter_fn is not None:
            files_to_be_download = self.ls(src, filter_fn=filter_fn)
            for i, file in enumerate(files_to_be_download):
                if (max_num is not None) and (i >= max_num):
                    break
                self.download(file, dest, is_dir=False)
            return

        cmd = f"{self.cmd_prefix} cp {'-r' if is_dir else ''} {src} {dest}"
        self.info(cmd)
        res = []
        with os.popen(cmd, 'r') as fr:
            for line in fr:
                line = line.strip()
                res.append(line)
        return res

    def rm(self, path, is_dir=False):
        if self.replace_s3:
            path = path.replace("s3://", "oss://")
        cmd = f"{self.cmd_prefix} rm {'-r' if is_dir else ''} {path}"
        with os.popen(cmd, 'r') as fr:
            for line in fr:
                print(line)

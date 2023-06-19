#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
from pyutilb.cmd import *
from pyutilb.file import *
from pyutilb.util import replace_sysarg

# 配置文件
# config_file = '~/.kube/k8scmd.yml'
config_file = os.environ['HOME'] + '/.kube/k8scmd.yml'
# 默认配置
default_config = {
    'get-output': 'wide', # 输出格式
    'get-labels': False, # 是否显示标签
    'get-ns': '' # 命名空间，默认显示全部
}

# 读配置
def read_config():
    if not os.path.exists(config_file):
        write_file(config_file, yaml.dump(default_config))
    return read_yaml(config_file)

# 写配置
def write_config(config):
    #config = dict(default_config, **config)
    # config = {**default_config, **config}
    write_file(config_file, yaml.dump(config))

# 执行命令
def run_cmd(cmd):
    cmd = replace_sysarg(cmd)
    print(cmd)
    os.system(cmd)

# 执行k8s资源的get/describe/delete命令
def run_res_cmd(res):
    cmd = get_res_cmd(res)
    run_cmd(cmd)

# 生成k8s资源的get/describe/delete命令
def get_res_cmd(res):
    deleting = has_delete_arg()
    name = get_res_name(res, False)
    # 1 delete
    if deleting:
        return f'kubectl delete {res} {name} $2_'

    # 2 有资源名: describe 详情
    if name is not None:
        return f'kubectl describe {res} {name} $2_'

    # 3 无资源名: get 列表
    # 根据配置构建显示选项
    config = read_config()
    # option = '-o wide --get-labels'
    option = ''
    if '-o' not in sys.argv:
        option = f"-o {config['get-output']}"
    if config['get-labels']:
        option += ' --show-labels'
    # 过滤命名空间
    if config['get-ns']:
        ns = f"-n {config['get-ns']}"
    else:
        ns = '-A'
    # 拼接命令
    return f'kubectl get {res} {ns} {option} $1_'

# 从命令行参数选出并删掉 -d
def has_delete_arg():
    ret = '-d' in sys.argv
    if ret: # 删除
        sys.argv.remove('-d')
    return ret

# 从命令行参数中资源名
def get_res_name(res, required = True):
    if len(sys.argv) == 1:  # 无资源名参数
        if required:
            raise Exception('缺少资源名参数')
        return None

    name = sys.argv[1]
    if name.startswith('-'): # get命令，如 -o yaml，是拿不到资源名的
        return None
    if res != 'no' and res != 'ns': # 一般资源需带命名空间
        name = name + ' -n ' + get_ns(res, name)
    return name

# 找到某个资源的命名空间
def get_ns(res, name):
    df = run_command_return_dataframe(f"kubectl get {res} -A -o wide")
    name2ns = dict(zip(df['NAME'], df['NAMESPACE']))
    if name in name2ns:
        return name2ns[name]
    raise Exception(f'找不到资源[{name}]的命名空间')
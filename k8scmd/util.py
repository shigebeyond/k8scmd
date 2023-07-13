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
    name = get_res_name(res, False)
    # 1 delete
    if has_delete_arg():
        return f'kubectl delete {res} {name} $2_'

    # 2 edit
    if has_edit_arg():
        return f'kubectl edit {res} {name} $2_'

    # 3 有资源名或babel(以-l开头): describe 详情
    if name is not None and not name.startswith('-l '):
        if '-o' in sys.argv: # 有指定输出就用get
            return f'kubectl get {res} {name} $2_'
        # 否则用 describe
        return f'kubectl describe {res} {name} $2_'

    # 4 无资源名: get 列表
    option = build_show_option()

    # 4.3 过滤标签
    labels = '' # 标签
    other_args = '$1_' # 其他参数
    if name is not None and name.startswith('-l '):
        labels = ' ' + name
        other_args = '$2_'

    # 拼接命令
    return f'kubectl get {res}{labels} {option} {other_args}'

# 根据配置构建显示选项
def build_show_option():
    config = read_config()
    # option = '-o wide --get-labels'
    # 4.1 过滤命名空间
    if config['get-ns']:
        option = f"-n {config['get-ns']}"
    else:
        option = '-A'
    # 4.2 输出格式
    if '-o' not in sys.argv:
        option += f" -o {config['get-output']}"
    # 4.3 显示标签
    if config['get-labels']:
        option += ' --show-labels'
    return option


# 从命令行参数选出并删掉 -d
def has_delete_arg():
    return has_and_remove_arg('-d')

# 从命令行参数选出并删掉 -e
def has_edit_arg():
    return has_and_remove_arg('-e')

# 从命令行参数选出并删掉指定参数
def has_and_remove_arg(arg):
    ret = arg in sys.argv
    if ret:  # 删除
        sys.argv.remove(arg)
    return ret

res_without_ns = ['no' , 'ns' , 'cs' , 'pv'] # 不带命名空间的资源

# 从命令行参数中资源名或label
def get_res_name(res, required = True):
    if len(sys.argv) == 1:  # 无资源名参数
        if required:
            raise Exception('缺少资源名参数')
        return None

    # 取第一个参数为资源名
    name = sys.argv[1]
    # get命令选项，如 -o yaml，是拿不到资源名的
    if name.startswith('-'):
        return None

    # label，其中 @ 是 app= 的缩写
    if name.startswith('@'):
        return f"-l app={name[1:]}"

    # 纯资源名，要带命名空间
    if res not in res_without_ns: # 只对带命名空间的资源
        if res == 'pod' and ':' in name: # podname:container
            name, container = name.split(':', 1)
        else:
            container = None
        name = name + ' -n ' + get_ns(res, name)
        if container:
            name += ' -c ' + container
    return name

# 找到某个资源的命名空间
def get_ns(res, name):
    df = run_command_return_dataframe(f"kubectl get {res} -A -o wide")
    name2ns = dict(zip(df['NAME'], df['NAMESPACE']))
    if name in name2ns:
        return name2ns[name]
    raise Exception(f'找不到{res}资源[{name}]的命名空间')

# ip对pod名的映射
ip2pod = None
# 根据ip找到pod名
def get_pod_by_ip(ip):
    global ip2pod
    if ip2pod is None:
        # 修正RESTARTS列中有`3 (97m ago)`，干掉括号
        def fix_output(o):
            return re.sub(r'\(.+\)', '', o)  # 干掉括号
        df = run_command_return_dataframe(f"kubectl get pod -A -o wide", fix_output)
        ip2pod = dict(zip(df['IP'], df['NAME']))
    if ip in ip2pod:
        return ip2pod[ip]
    return None
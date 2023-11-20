#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import re
from pyutilb.cmd import *
from pyutilb.file import *
from pyutilb.ts import age2seconds
from pyutilb.util import replace_sysarg

# 修正k8s命令输出
def fix_k8s_cmd_output(cmd):
    # get pod命令输出的RESTARTS(重启次数)列有括号，如1 (9h ago) => 去掉
    def fix(output):
        if ' get pod' in cmd:
            return re.sub(r"\(.+\)", "", output)
        return output
    return fix

# 同步执行命令，并将输出整理为df + 修正k8s命令输出
def run_command_return_dataframe2(cmd):
    return run_command_return_dataframe(cmd, fix_k8s_cmd_output(cmd))

# --------------------------- k8s命令帮助方法 ---------------------------
# 配置文件
# config_file = '~/.kube/k8scmd.yml'
config_file = os.environ['HOME'] + '/.kube/k8scmd.yml'
# 默认配置
default_config = {
    'get-output': 'wide', # 输出格式
    'get-labels': False, # 是否显示标签
    'get-ns': '', # 命名空间，默认显示全部
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

# 执行k8s资源的get/describe/edit/delete增删改查命令
def run_res_crud_cmd(res):
    cmd = get_res_crud_cmd(res)
    run_cmd(cmd)

# 生成k8s资源的get/describe/edit/delete增删改查命令
def get_res_crud_cmd(res):
    name = get_res_name(res, False)
    # 1 delete
    if has_delete_arg():
        return f'kubectl delete {res} {name} $2_'

    # 2 edit
    if has_edit_arg():
        return f'kubectl edit {res} {name} $2_'

    # 3 有资源名或label(以-l开头): describe 详情
    if name is not None and not name.startswith('-l '):
        if '-o' in sys.argv: # 有指定输出就用get
            return f'kubectl get {res} {name} $2_'
        # 否则用 describe
        return f'kubectl describe {res} {name} $2_'

    # 4 无资源名: get 列表
    option = build_list_option()

    # 4.3 过滤标签
    labels = '' # 标签
    other_args = '$1_' # 其他参数
    if name is not None and name.startswith('-l '):
        labels = ' ' + name
        other_args = '$2_'

    # 拼接命令
    return f'kubectl get {res}{labels} {option} {other_args}'

# 根据配置构建list显示选项
def build_list_option():
    config = read_config()
    # option = '-o wide --get-labels'
    # 4.1 过滤命名空间
    option = build_ns_option(True)
    # 4.2 输出格式
    if '-o' not in sys.argv:
        option += f" -o {config['get-output']}"
    # 4.3 显示标签
    if config['get-labels']:
        option += ' --show-labels'
    return option

def build_ns_option(is_list):
    '''
    根据配置构建命名空间选项
    :param: is_list 是否是list命令
    '''
    config = read_config()
    option = ''
    if '-n' not in sys.argv and '-A' not in sys.argv:
        if config['get-ns']:
            option = f"-n {config['get-ns']}"
        elif is_list and not sys.argv[0].endswith('cwft'):
            option = '-A'
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
            name = get_latest_res_name(res)
            if name is None:
                raise Exception('缺少资源名参数')
            return name
        return None

    # 取第一个参数为资源名
    name = sys.argv[1]
    # get命令选项，如 -o yaml，是拿不到资源名的
    if name.startswith('-'):
        return None

    # 最新的资源
    if name == '@latest':
        return get_latest_res_name(res)

    # label，其中 @ 是 app= 的缩写
    if name.startswith('@'):
        return f"-l app={name[1:]}"

    # 纯资源名，要带命名空间
    if res == 'pod' and ':' in name: # podname:container
        name, container = name.split(':', 1)
    else:
        container = None
    if '*' in name: # 模糊搜索资源名
        name = search_res_name(res, name)
    elif res not in res_without_ns: # 精确资源名, 找到命名空间 -- 只对带命名空间的资源
        name = name + ' -n ' + get_res_ns(res, name)
    if container:
        name += ' -c ' + container
    return name

# 找到某个资源的命名空间
def get_res_ns(res, name):
    df = run_command_return_dataframe2(f"kubectl get {res} -A -o wide")
    name2ns = dict(zip(df['NAME'], df['NAMESPACE']))
    if name in name2ns:
        return name2ns[name]
    raise Exception(f'找不到{res}资源[{name}]的命名空间')

# 模糊搜索某个资源
def search_res_name(res, name):
    reg = name.replace('*', '.*')
    df = run_command_return_dataframe2(f"kubectl get {res} -A -o wide")
    # 如果是pod，则要对status排序，将Running状态提上去 => 优先取Running状态的pod
    if res == 'pod':
        df['sort'] = list(map(is_pod_running, df['STATUS']))
        df = df.sort_values(by='sort', ascending=False)
    # 匹配资源名
    for i, row in df.iterrows():
        if re.match(reg, row['NAME']):
            if res not in res_without_ns: # 只对带命名空间的资源
                return row['NAME'] + ' -n ' + row['NAMESPACE']
            return row['NAME']
    raise Exception(f'模糊搜索不到{res}资源[{name}]')

# 找到最新的资源名: 按age升序第一个为最新
def get_latest_res_name(res):
    df = run_command_return_dataframe2(f"kubectl get {res} -A -o wide")
    if len(df) == 0:
        return None
    # 对age排序
    df['sort'] = list(map(age2seconds, df['AGE']))
    df = df.sort_values(by='sort', ascending=True)
    row = df.iloc[0]
    return row['NAME'] + ' -n ' + row['NAMESPACE']

def is_pod_running(status):
    return int(status == 'Running')

# ip对pod名的映射
ip2pod = None
# 根据ip找到pod名
def get_pod_by_ip(ip):
    global ip2pod
    if ip2pod is None:
        # 修正RESTARTS列中有`3 (97m ago)`，干掉括号
        def fix_output(o):
            return re.sub(r'\(.+\)', '', o)  # 干掉括号
        df = run_command_return_dataframe2(f"kubectl get pod -A -o wide", fix_output)
        ip2pod = dict(zip(df['IP'], df['NAME']))
    if ip in ip2pod:
        return ip2pod[ip]
    return None

# --------------------------- argo命令帮助方法 ---------------------------
def run_argo_crud_cmd(type):
    '''
    执行argo的list/get/delete增删改查命令
    :param type: 类型，如空或wf表示流程, cwf表示定时流程, wftmpl表示流程模板
    :return:
    '''
    cmd = get_argo_crud_cmd(type)
    run_cmd(cmd)

def get_argo_crud_cmd(type):
    '''
    生成argo的list/get/delete增删改查命令
    :param type: 类型，如空或wf表示流程, cwf表示定时流程, wftmpl表示流程模板
    :return:
    '''
    cmd_pref = get_argo_cmd_pref(type)
    # list选项
    list_option = build_list_option()
    if len(sys.argv) == 1:  # 无流程名
        return f'{cmd_pref} list {list_option}'

    #name = sys.argv[1]
    name = get_argo_name(type, False)
    if name is None:
        return f'{cmd_pref} list {list_option} $1_'

    # 有label(以-l开头): list
    if name.startswith('-l '):
        return f'{cmd_pref} list -A {name} $2_'

    # 1 delete
    if has_delete_arg():
        return f'{cmd_pref} delete {name} $2_'

    # 2 有资源名: get 详情
    return f'{cmd_pref} get {name} $2_'

def get_argo_cmd_pref(type):
    '''
    获得argo命令前缀
    :param type: 类型，如空或wf表示流程, cwf表示定时流程, wftmpl/wft表示流程模板, cwft表示集群级流程模板
    :return:
    '''
    if type == 'cwf':
        cmd_pref = 'argo cron'
    elif type == 'wftmpl' or type == 'wft':
        cmd_pref = 'argo template'
    elif type == 'cwft':
        cmd_pref = 'argo cluster-template'
    else:
        cmd_pref = 'argo'
    return cmd_pref

# 从命令行参数中流程名
def get_argo_name(type, required = True):
    if len(sys.argv) == 1:  # 无流程名参数, 默认给 @latest(最新的流程)
        if required:
            return '@latest ' + build_ns_option(False)
        return None

    # 取第一个参数为流程名
    name = sys.argv[1]
    # get命令选项，如 -o yaml，是拿不到流程名的
    if name.startswith('-'):
        return None

    # label，其中 @ 是 app= 的缩写
    if name.startswith('@') and name != '@latest':
        return f"-l flow={name[1:]}"

    if ':' in name: # flowname:container
        name, container = name.split(':', 1)
    else:
        container = None
    # 纯流程名，要带命名空间
    if '*' in name: # 模糊搜索流程名
        name = search_argo_name(type, name)
    elif '@latest' != name: # 精确流程名, 找到命名空间
        name = name + ' -n ' + get_argo_ns(type, name)
    if container:
        name += ' -c ' + container
    return name

# 模糊搜索某个流程
def search_argo_name(type, name):
    cmd_pref = get_argo_cmd_pref(type)
    reg = name.replace('*', '.*')
    df = run_command_return_dataframe2(f"{cmd_pref} list -A")
    # 匹配流程名
    ret = []
    for i, row in df.iterrows():
        if re.match(reg, row['NAME']):
            name = row['NAME'] + ' -n ' + row['NAMESPACE']
            ret.append(name)
    n = len(ret)
    if n == 0:
        raise Exception(f'模糊搜索不到流程[{name}]')
    if n == 1:
        return ret[0]
    lines = [f"{i+1}. {v}" for i, v in enumerate(ret)]
    i = input("找到多个流程: \n" + "\n".join(lines) + "\n请输入序号选择以上一个流程: ")
    i = int(i) - 1
    if i < 0 or i >= n:
        raise Exception("无效流程序号")
    return ret[i]

# 找到某个流程的命名空间
def get_argo_ns(type, name):
    cmd_pref = get_argo_cmd_pref(type)
    df = run_command_return_dataframe2(f"{cmd_pref} list -A")
    name2ns = dict(zip(df['NAME'], df['NAMESPACE']))
    if name in name2ns:
        return name2ns[name]
    raise Exception(f'找不到流程[{name}]的命名空间')

if __name__ == '__main__':
    print(get_res_name("pod", required=True))
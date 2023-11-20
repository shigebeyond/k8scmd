#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
from pyutilb.strs import substr_after_last
from k8scmd.util import *

# --------------------------- k8s命令 ---------------------------
'''
k8s命令简写
命名参考 k8s资源简写: https://zhuanlan.zhihu.com/p/369647740
'''
def k8sstart():
    cmd = '''sudo swapoff -a
sudo systemctl restart kubelet
kubectl get nodes'''
    run_cmd(cmd)

def k8sstop():
    cmd = 'sudo systemctl stop kubelet'
    run_cmd(cmd)

def k8scluster():
    # 集群状态
    # run_res_cmd('cs')
    cmd = get_res_crud_cmd('cs')
    if ' get ' in cmd and ' -o wide' in cmd:
        run_cmd('kubectl cluster-info') # 先输出集群信息
        print("\n--------------------------------\n")
    run_cmd(cmd)

# 查看所有资源
def k8sall():
    option = build_list_option()
    run_cmd(f'kubectl get all {option}')

def k8sns():
    run_res_crud_cmd('ns')

def k8sno():
    run_res_crud_cmd('no')

def k8spod():
    run_res_crud_cmd('pod')

def k8ssvc():
    run_res_crud_cmd('svc')

def k8swf():
    run_res_crud_cmd('wf')

def k8swft():
    run_res_crud_cmd('wftmpl')

def k8scwft():
    run_res_crud_cmd('cwft')

def k8scwf():
    run_res_crud_cmd('cwf')

def k8swfevent():
    run_res_crud_cmd('WorkflowEventBinding')

# 输出每个服务的服务url+终端url
def k8ssvcurl():
    cmd = get_res_crud_cmd('svc')
    # get转pandas，并构建http url列，方便用户复制url
    if ' get ' in cmd:
        cmd = replace_sysarg(cmd)
        print(cmd)
        df = run_command_return_dataframe2(cmd)
        # 拼接url
        service_urls = [] # 服务url
        endpoint_urls = [] # 终端的url
        for i, row in df.iterrows():
            service_urls.append(build_service_url(row))
            endpoint_urls.append(build_endpoint_url(row))
        df['SVC-URL'] = service_urls
        df['ENDPOINT-URL'] = endpoint_urls
        del df['CLUSTER-IP']
        del df['EXTERNAL-IP']
        del df['PORT(S)']
        del df['AGE']
        del df['SELECTOR']
        print(df)
        return
    run_cmd(cmd)

# 构建服务url
def build_service_url(row):
    ip = row['CLUSTER-IP']
    ports = re.findall(f'[\d:]+(?=\/)', row['PORT(S)'])
    urls = []
    for port in ports:
        if ':' in port:  # ServicePort:NodePort
            port, _ = port.split(':')
        port = int(port)
        if port != 443 and port != 53:
            url = f"{ip}:{port}"
            urls.append(url)
    return ','.join(urls)

# 构建终端url
def build_endpoint_url(row):
    cmd = f"kubectl describe svc {row['NAME']} -n {get_row_ns(row)}"
    output = run_command(cmd)
    mat = re.search(f'Endpoints:\s*(.+)\n', output)
    ret = mat.group(1)
    return ret
    # return add_pod_by_ip(ret)

# 对ip字符串添加pod名
def add_pod_by_ip(endpoints):
    def add_pod(mat):
        ip = mat.group(1)
        pod = get_pod_by_ip(ip)
        if pod is None:
            return ip
        return f"({pod}){ip}"
    return re.sub(r'(\d+.\d+.\d+.\d+):', add_pod, endpoints)  # 对ip字符串添加pod名

def collect_pod_by_ips(endpoints, has_port = True):
    '''
    对ip字符串收集pod名
    :param endpoints: 终端列表，只能包含ip端口逗号，不能包含其他字符
    :param has_port: 是否包含端口
    :return:
    '''
    port_reg = ''
    if has_port:
        port_reg = ':\d+'
    ips = re.findall(rf'(\d+.\d+.\d+.\d+){port_reg}', endpoints)
    ips = set(ips) # 去重
    return ','.join(list(map(get_pod_by_ip, ips)))

# 获得指定行中的命名空间，如果行中没有，则取配置的默认命名空间
def get_row_ns(row):
    if 'NAMESPACE' in row:
        return row['NAMESPACE']
    # 取配置的默认命名空间
    return read_config()['get-ns']

# 对指定服务url执行curl命令
def k8ssvccurl():
    name = get_res_name('svc')
    res = run_command_return_yaml(f"kubectl get svc {name} -o yaml")
    ip = res['spec']['clusterIP']
    # 遍历每个端口来执行curl
    for p in res['spec']['ports']:
        port = p['port']
        if port != 443 and port != 53:
            curl = f"curl {ip}:{port}"
            # run_cmd(curl)
            print(f"执行命令: {curl}, 结果如下")
            os.system(curl)
            print()

# 输出每个服务的终端对应的pod
def k8ssvcpod():
    cmd = get_res_crud_cmd('endpoints')
    # get转pandas，并构建http url列，方便用户复制url
    if ' get ' in cmd:
        cmd = replace_sysarg(cmd)
        print(cmd)
        df = run_command_return_dataframe2(cmd)
        # 拼接url
        # eps = list(map(add_pod_by_ip, df['ENDPOINTS'])) # 终端加pod -- 显示不全
        # df['ENDPOINTS'] = eps
        pods = []
        for i, row in df.iterrows():
            pods.append(collect_pod_by_ips(row['ENDPOINTS']))
        df['POD'] = pods
        del df['AGE']
        print(df)
        return
    if ' describe ' in cmd:
        cmd = replace_sysarg(cmd)
        print(cmd)
        o = run_command(cmd)
        def add_pods(mat):
            ips = mat.group(2)
            pods = collect_pod_by_ips(ips, False)
            pref = mat.group(1)
            return f"{pref}{ips}\n{pref.replace('Addresses', 'Pods')}{pods}\n"
        o = re.sub(r'( *Addresses: *)((\d+.\d+.\d+.\d+.?)+)\n', add_pods, o)  # 对ip字符串添加pod名
        print(o)
        return
    run_cmd(cmd)

def k8src():
    run_res_crud_cmd('rc')

def k8srs():
    run_res_crud_cmd('rs')

def k8sds():
    run_res_and_rollout_cmd('ds')

def k8ssts():
    run_res_and_rollout_cmd('sts')

def k8sdeploy():
    run_res_and_rollout_cmd('deploy')

# 执行资源+rollout命令(暂停或恢复部署)，用在 deploy + ds + sts
def run_res_and_rollout_cmd(res):
    # 1 执行rollout命令: 暂停或恢复部署，应用在 deploy + ds + sts
    action = get_rollout_action() # 获得rollout命令的动作
    if action:
        name = get_res_name(res)
        cmd = f'kubectl rollout {action} {res} {name}'
        run_cmd(cmd)
        return

    # 2 查看部署：kubectl get/describe deploy
    # run_res_cmd(res)
    cmd = get_res_crud_cmd(res)
    run_cmd(cmd)

    # 3 查看部署状态： kubectl rollout status deploy
    if ' describe ' in cmd:
        print("\n--------------------------------\n")
        name = get_res_name(res)
        cmd = f'kubectl rollout status {res} {name}'
        run_cmd(cmd)

rollout_actions = ['history', 'pause', 'restart', 'resume', 'status', 'undo']

def get_rollout_action():
    '''
    获得rollout命令的动作
        history: 显示上线历史
        pause: 将所指定的资源标记为已暂停
        restart: Restart a resource
        resume: 恢复暂停的资源
        status: 显示上线的状态
        undo: 撤销上一次的上线
    '''
    action = None
    if len(sys.argv) >= 3:
        action = sys.argv[2]
        if action == 'start':  # 恢复部署
            action = 'resume'
        elif action == 'stop':  # 暂停部署
            action = 'pause'
        # restart: 重启pod
    if action in rollout_actions:
        return action
    return None

def k8shpa():
    run_res_crud_cmd('hpa')

def k8sconfig():
    run_res_crud_cmd('cm')

def k8ssecret():
    run_res_crud_cmd('secret')

def k8sendpoint():
    run_res_crud_cmd('endpoints')

def k8sevent():
    run_res_crud_cmd('events')

def k8sjob():
    run_res_crud_cmd('jobs')

def k8sing():
    run_res_crud_cmd('ingresses')

def k8singrule():
    cmd = get_res_crud_cmd('ing')
    # get转pandas，逐个输出rule
    if ' get ' in cmd:
        cmd = replace_sysarg(cmd)
        print(cmd)
        df = run_command_return_dataframe2(cmd)
        for i, row in df.iterrows():
            print('----------------------------')
            print(f"{i+1}. {row['NAME']} -n {get_row_ns(row)}")
            print(build_ingress_rule(row))
        return
    run_cmd(cmd)

# 构建ingress rule
def build_ingress_rule(row):
    cmd = f"kubectl describe ing {row['NAME']} -n {get_row_ns(row)}"
    output = run_command(cmd)
    mat = re.search(f'Rules:\n(.+)\nAnnotations:', output, re.S)
    ret = mat.group(1)
    return ret
    # return add_pod_by_ip(ret)

def k8scron():
    k8scronjob()

def k8scronjob():
    run_res_crud_cmd('cronjobs')

def k8spv():
    run_res_crud_cmd('pv')

def k8spvc():
    run_res_crud_cmd('pvc')

def k8saccount():
    run_res_crud_cmd('serviceaccount')

def k8srole():
    run_res_crud_cmd('role')

def k8srolebind():
    run_res_crud_cmd('rolebinding')

def k8scrole():
    run_res_crud_cmd('clusterrole')

def k8scrolebind():
    run_res_crud_cmd('clusterrolebinding')

# storageclasses
def k8ssc():
    run_res_crud_cmd('storageclasses')

def k8sexec():
    name = get_res_name('pod')
    run_cmd(f'kubectl exec -it {name} -- $2_')

def k8sbash():
    name = get_res_name('pod')
    run_cmd(f'kubectl exec -it {name} -- bash')

def k8ssh():
    name = get_res_name('pod')
    run_cmd(f'kubectl exec -it {name} -- sh')

def k8slog():
    name = get_res_name('pod')
    all_container = ''
    if not ('-c' in sys.argv or ' -c ' in name): # 不带具体容器名
        all_container = '--all-containers=true' # 看所有容器的日志
    run_cmd(f"kubectl logs {name} {all_container} $2_")

def k8sletlog():
    run_cmd("sudo journalctl -u kubelet | tail -n 50")

def build_apply_files():
    # return sys.argv[1] # 可能有多个文件，如对参数 namenode*.yml，命令会拿到多个文件
    files = sys.argv[1:]
    return ' -f '.join(files)

def k8sapply():
    #run_cmd("kubectl apply --record=true -f $1_")
    run_cmd("kubectl apply --record=true -f " + build_apply_files())

def k8screate():
    run_cmd("kubectl create -f " + build_apply_files())

def k8sdelete():
    run_cmd("kubectl delete -f " + build_apply_files())

def k8sdiff():
    run_cmd("kubectl diff -f " + build_apply_files())

def k8sscale():
    # deploy资源名
    name = get_res_name('deploy')
    if len(sys.argv) < 3 or not sys.argv[2].isdigit():
            raise Exception(f'第2个参数必须是int类型的副本数, 而传入的是{sys.argv[2]}')
    # 执行命令
    run_cmd(f"kubectl scale deploy {name} --replicas={sys.argv[2]}")

def k8shistory():
    # deploy资源名
    name = get_res_name('deploy')
    # 命令
    cmd = f"kubectl rollout history deploy {name}"
    # 检查是否有指定版本: 第2个参数
    version = get_deploy_version()
    if version:
        cmd += ' --revision=' + version
    run_cmd(cmd)

def k8srollback():
    # deploy资源名
    name = get_res_name('deploy')
    # 命令
    cmd = f"kubectl rollout undo deploy {name}"
    # 检查是否有指定版本: 第2个参数
    version = get_deploy_version()
    if version:
        cmd += ' --to-revision=' + version
    run_cmd(cmd)

# 获得deploy的版本参数
def get_deploy_version():
    version = None
    if len(sys.argv) >= 3:
        version = sys.argv[2]
        if not version.isdigit():
            raise Exception(f'第2个参数必须是int类型的版本号, 而传入的是{version}')
    return version

# 切换是否显示标签
def k8sgetlabels():
    config = read_config()
    config['get-labels'] = not config['get-labels']
    write_config(config)
    print(f"Set get-labels={config['get-labels']}")

# 指定输出格式
def k8sgetoutput():
    config = read_config()
    if len(sys.argv) == 1: # 无指定格式，则在wide,yaml之间切换
        if config['get-output'] == 'yaml':
            of = 'wide'
        else:
            of = 'yaml'
    else:
        of = sys.argv[1]
    config['get-output'] = of
    write_config(config)
    print(f"Set get-output={config['get-output']}")

# 指定查看的命名空间：只查看该命名空间的资源
def k8sgetns():
    config = read_config()
    if len(sys.argv) == 1:  # 无指定命名空间，则全部
        of = ''
    else:
        of = sys.argv[1]
    config['get-ns'] = of
    write_config(config)
    print(f"Set get-ns={config['get-ns']}")

def k8sapi():
    if len(sys.argv) == 1: # 无资源类型
        run_cmd(f"kubectl api-resources")
        return

    # 有资源类型
    run_cmd(f"kubectl explain {sys.argv[1]} --recursive")

def k8sbuild():
    '''
    使用docker构建镜像，并导入到k8s中
    docker build -t my-app .
    docker save my-app -o my-app.tar
    ctr -n k8s.io images import my-app.tar'''
    # 打包的镜像名
    img = file = ''
    for i in range(0, len(sys.argv)):
        if sys.argv[i] == '-t':
            img = file = sys.argv[i+1]
            if '/' in file: # 192.168.0.182:5000/rpcserver:3.0.0
                file = substr_after_last(file, '/').replace(':', '-')
    if not img:
        raise Exception('没指定镜像名, 请参考docker build -h')
    # 执行命令
    cmd = f'''sudo docker build $1_
    sudo docker save {img} -o {file}.tar
    sudo ctr -n k8s.io images import {file}.tar'''
    run_cmd(cmd)

def k8sexport():
    '''
    k8s导出镜像
    ctr -n k8s.io images export mysql.tar docker.io/library/mysql:5.7-debian --platform linux/amd64
    '''
    img = file = sys.argv[1]
    if '/' in file: # 192.168.0.182:5000/rpcserver:3.0.0
        file = substr_after_last(file, '/').replace(':', '-')
    cmd = f"sudo ctr -n k8s.io images export {file}.tar {img} --platform linux/amd64"
    run_cmd(cmd)

def k8simport():
    '''
    导入镜像
    ctr -n k8s.io images import mysql.tar
    '''
    file = sys.argv[1]
    cmd = f"sudo ctr -n k8s.io images import {file}"
    run_cmd(cmd)

# --------------------------- argo命令 ---------------------------
# ------------- 通用命令 -------------
def argo_create(type):
    cmd_pref = get_argo_cmd_pref(type)
    run_cmd(f"{cmd_pref} create {build_ns_option(False)} $1_")

def argo_resume(type):
    name = get_argo_name(type)
    cmd_pref = get_argo_cmd_pref(type)
    run_cmd(f"{cmd_pref} resume {name} $2_")

def argo_suspend(type):
    name = get_argo_name(type)
    cmd_pref = get_argo_cmd_pref(type)
    run_cmd(f"{cmd_pref} suspend {name} $2_")

# ------------- 流程相关命令 -------------
def wf():
    run_argo_crud_cmd('wf')

def wfsubmit():
    w = ''
    if '--watch' not in sys.argv:
        w = '--watch'
    run_cmd(f"argo submit {build_ns_option(False)} $1_ {w}")

# 删除所有流程
def wfclear():
    r = input("Are you delete all workflow? (Y/N) ").lower()
    if r == 'y' or r == 'yes':
        run_cmd("argo delete -A")

def wflog():
    name = get_argo_name('wf')
    run_cmd(f"argo logs {name} $2_")

def wfretry():
    name = get_argo_name('wf')
    run_cmd(f"argo retry {name} $2_")

def wfresume():
    argo_resume('wf')

def wfsuspend():
    argo_suspend('wf')

# ------------- 定时流程相关命令 -------------
def cwf():
    run_argo_crud_cmd('cwf')

def cwfcreate():
    argo_create('cwf')

def cwfresume():
    argo_resume('cwf')

def cwfsuspend():
    argo_suspend('cwf')

# ------------- 流程模板相关命令 -------------
def wft():
    run_argo_crud_cmd('wft')

def wftcreate():
    argo_create('wft')

# ------------- 集群级流程模板相关命令 -------------
def cwft():
    run_argo_crud_cmd('cwft')

def cwftcreate():
    argo_create('cwft')

# 测试
if __name__ == '__main__':
    # k8spod()
    # k8sexec()
    # k8sbash()
    # k8ssvc()
    # k8singrule()
    # k8ssvcpod()
    # k8sbuild()
    cwft()
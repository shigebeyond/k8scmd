#!/usr/bin/python3
# -*- coding: utf-8 -*-

from k8scmd.util import *

'''
k8s命令简写
命名参考 k8s资源简写: https://zhuanlan.zhihu.com/p/369647740
'''

def k8sstart():
    cmd = '''sudo swapoff -a
sudo systemctl restart kubelet
kubectl get nodes'''
    run_cmd(cmd)

def k8sns():
    run_res_cmd('ns')

def k8sno():
    run_res_cmd('no')

def k8spod():
    run_res_cmd('pod')

def k8ssvc():
    run_res_cmd('svc')

def k8ssvc2():
    cmd = get_res_cmd('svc')
    # get转pandas，并构建http url列，方便用户复制url
    if ' get ' in cmd:
        cmd = replace_sysarg(cmd)
        print(cmd)
        url_col = []
        df = run_command_return_dataframe(cmd)
        for i, row in df.iterrows():
            ip = row['CLUSTER-IP']
            ports = re.findall(f'\d+(?=\/)', row['PORT(S)'])
            urls = []
            for port in ports:
                port = int(port)
                if port >= 30000:
                    url = f"http://{ip}:{port}"
                    urls.append(url)
            url_col.append(','.join(urls))
        df['url'] = url_col
        print(df)
        return
    run_cmd(cmd)

def k8src():
    run_res_cmd('rc')

def k8srs():
    run_res_cmd('rs')

def k8sds():
    run_res_cmd('ds')

def k8ssts():
    run_res_cmd('sts')

def k8sdeploy():
    # 1 暂停或恢复部署
    if len(sys.argv) >= 3:
        action = sys.argv[2]
        if action == 'start': # 恢复部署
            action = 'resume'
        elif action == 'stop': # 暂停部署
            action = 'pause'
        elif action == 'restart': # 重启pod
            action = 'restart'
        else:
            action = None
        if action:
            name = get_res_name('deploy')
            cmd = f'kubectl rollout {action} deploy {name}'
            run_cmd(cmd)
            return

    # 2 查看部署：kubectl get/describe deploy
    # run_res_cmd('deploy')
    cmd = get_res_cmd('deploy')
    run_cmd(cmd)

    # 3 查看部署状态： kubectl rollout status deploy
    if ' describe ' in cmd:
        print("\n--------------------------------\n")
        name = get_res_name('deploy')
        cmd = f'kubectl rollout status deploy {name}'
        run_cmd(cmd)

def k8sconfig():
    run_res_cmd('cm')

def k8ssecret():
    run_res_cmd('secret')

def k8sendpoint():
    run_res_cmd('endpoints')

def k8sevent():
    run_res_cmd('events')

def k8sjob():
    run_res_cmd('jobs')

def k8singress():
    run_res_cmd('ingresses')

def k8scronjob():
    run_res_cmd('cronjobs')

def k8spv():
    run_res_cmd('pv')

def k8spvc():
    run_res_cmd('pvc')

# storageclasses
def k8ssc():
    run_res_cmd('storageclasses')

def k8sexec():
    name = get_res_name('pod')
    run_cmd(f'kubectl exec -it {name} -- $2_')

def k8sbash():
    name = get_res_name('pod')
    run_cmd(f'kubectl exec -it {name} -- bash')

def k8slog():
    name = get_res_name('pod')
    run_cmd(f"kubectl logs {name} $2_")

def k8sletlog():
    run_cmd("sudo journalctl -u kubelet | tail -n 50")

def k8screate():
    run_cmd("kubectl create -f $1_")

def k8sapply():
    run_cmd("kubectl apply --record=true -f $1_")

def k8sdelete():
    run_cmd("kubectl delete -f $1_")

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
def k8sshowlabel():
    config = read_config()
    config['show-labels'] = not config['show-labels']
    write_config(config)
    print(f"Set show-labels={config['show-labels']}")

# 指定输出格式
def k8soutput():
    config = read_config()
    if len(sys.argv) == 1: # 无指定格式，则在wide,yaml之间切换
        if config['output-format'] == 'yaml':
            of = 'wide'
        else:
            of = 'yaml'
    else:
        of = sys.argv[1]
    config['output-format'] = of
    write_config(config)
    print(f"Set output-format={config['output-format']}")

# 测试
if __name__ == '__main__':
    # k8sexec()
    k8ssvc()
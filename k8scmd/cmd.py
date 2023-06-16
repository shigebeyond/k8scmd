#!/usr/bin/python3
# -*- coding: utf-8 -*-

from k8scmd.util import *

'''
k8s命令简写
命名参考 k8s资源简写: https://zhuanlan.zhihu.com/p/369647740
'''

def k8sstart():
    cmd = '''
sudo swapoff -a
sudo systemctl restart kubelet
kubectl get nodes
'''
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
    run_res_cmd('deploy')

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
    run_cmd("kubectl apply -f $1_")

def k8sdelete():
    run_cmd("kubectl delete -f $1_")

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
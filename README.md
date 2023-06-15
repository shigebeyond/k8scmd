[GitHub](https://github.com/shigebeyond/k8scmd) | [Gitee](https://gitee.com/shigebeyond/k8scmd)

# k8scmd - k8s命令精简版
## 概述
k8s命令很多，难记又难打，非常艰难；
我直接用python做了一个简化版的命令，易记又易打，非常简单。

- 目前仅支持linux环境，windows环境未测试

## 安装
```
pip install k8scmd
```

## 使用
1. k8sstart: 启动 kubelet 服务
```
k8sstart
```

2. k8sns: 查看或删除 Namespace
```sh
# 查看所有Namespace资源列表
k8sns
k8sns -o yaml
# 查看单个Namespace资源详情
k8sns 资源名
# 删除单个Namespace资源
k8sns 资源名 -d
```

3. k8sno: 查看或删除 Node
```sh
# 查看所有Node资源列表
k8sno
k8sno -o yaml
# 查看单个Node资源详情
k8sno 资源名
# 删除单个Node资源
k8sno 资源名 -d
```

4. k8spod: 查看或删除 Pod
```sh
# 查看所有Pod资源列表
k8spod
k8spod -o yaml
# 查看单个Pod资源详情
k8spod 资源名
# 删除单个Pod资源
k8spod 资源名 -d
```

5. k8ssvc: 查看或删除 Service
```sh
# 查看所有Service资源列表
k8ssvc
k8ssvc -o yaml
# 查看单个Service资源详情
k8ssvc 资源名
# 删除单个Service资源
k8ssvc 资源名 -d
```

6. k8src: 查看或删除 ReplicationController
```sh
# 查看所有ReplicationController资源列表
k8src
k8src -o yaml
# 查看单个ReplicationController资源详情
k8src 资源名
# 删除单个ReplicationController资源
k8src 资源名 -d
```

7. k8srs: 查看或删除 ReplicaSet
```sh
# 查看所有ReplicaSet资源列表
k8srs
k8srs -o yaml
# 查看单个ReplicaSet资源详情
k8srs 资源名
# 删除单个ReplicaSet资源
k8srs 资源名 -d
```

8. k8sds: 查看或删除 DaemonSet
```sh
# 查看所有DaemonSet资源列表
k8sds
k8sds -o yaml
# 查看单个DaemonSet资源详情
k8sds 资源名
# 删除单个DaemonSet资源
k8sds 资源名 -d
```

9. k8ssts: 查看或删除 StatefulSet
```sh
# 查看所有StatefulSet资源列表
k8ssts
k8ssts -o yaml
# 查看单个StatefulSet资源详情
k8ssts 资源名
# 删除单个StatefulSet资源
k8ssts 资源名 -d
```

10. k8sdeploy: 查看或删除 Deployment
```sh
# 查看所有Deployment资源列表
k8sdeploy
k8sdeploy -o yaml
# 查看单个Deployment资源详情
k8sdeploy 资源名
# 删除单个Deployment资源
k8sdeploy 资源名 -d
```

11. k8sconfig: 查看或删除 ConfigMap
```sh
# 查看所有ConfigMap资源列表
k8sconfig
k8sconfig -o yaml
# 查看单个ConfigMap资源详情
k8sconfig 资源名
# 删除单个ConfigMap资源
k8sconfig 资源名 -d
```

12. k8ssecret: 查看或删除 Secret
```sh
# 查看所有Secret资源列表
k8ssecret
k8ssecret -o yaml
# 查看单个Secret资源详情
k8ssecret 资源名
# 删除单个Secret资源
k8ssecret 资源名 -d
```

13. k8sendpoint: 查看或删除 Endpoint
```sh
# 查看所有Endpoint资源列表
k8sendpoint
k8sendpoint -o yaml
# 查看单个Endpoint资源详情
k8sendpoint 资源名
# 删除单个Endpoint资源
k8sendpoint 资源名 -d
```

14. k8sevent: 查看或删除 Event
```sh
# 查看所有Event资源列表
k8sevent
k8sevent -o yaml
# 查看单个Event资源详情
k8sevent 资源名
# 删除单个Event资源
k8sevent 资源名 -d
```

15. k8sjob: 查看或删除 Job
```sh
# 查看所有Job资源列表
k8sjob
k8sjob -o yaml
# 查看单个Job资源详情
k8sjob 资源名
# 删除单个Job资源
k8sjob 资源名 -d
```

16. k8singress: 查看或删除 Ingress
```sh
# 查看所有Ingress资源列表
k8singress
k8singress -o yaml
# 查看单个Ingress资源详情
k8singress 资源名
# 删除单个Ingress资源
k8singress 资源名 -d
```

17. k8scronjob: 查看或删除 Cronjob
```sh
# 查看所有Cronjob资源列表
k8scronjob
k8scronjob -o yaml
# 查看单个Cronjob资源详情
k8scronjob 资源名
# 删除单个Cronjob资源
k8scronjob 资源名 -d
```

18. k8spv: 查看或删除 PersistentVolume
```sh
# 查看所有PersistentVolume资源列表
k8spv
k8spv -o yaml
# 查看单个PersistentVolume资源详情
k8spv 资源名
# 删除单个PersistentVolume资源
k8spv 资源名 -d
```

19. k8spvc: 查看或删除 PersistentVolumeClaim
```sh
# 查看所有PersistentVolumeClaim资源列表
k8spvc
k8spvc -o yaml
# 查看单个PersistentVolumeClaim资源详情
k8spvc 资源名
# 删除单个PersistentVolumeClaim资源
k8spvc 资源名 -d
```

20. k8ssc: 查看或删除 StorageClass
```sh
# 查看所有StorageClass资源列表
k8ssc
k8ssc -o yaml
# 查看单个StorageClass资源详情
k8ssc 资源名
# 删除单个StorageClass资源
k8ssc 资源名 -d
```

21. k8sexec: 在pod中执行命令
```sh
k8sexec Pod资源名 命令
# 例如
k8sexec nginx ls -l
```

22. k8sbash: 进入pod bash
```sh
k8sbash Pod资源名
# 例如
k8sbash nginx
```


23. k8slog: 查看pod日志
```sh
k8slog Pod资源名
# 例如
k8slog nginx
```

24. k8sletlog: 查看kubelet服务日志
```sh
k8sletlog
k8sletlog -f
```

25. k8screate: 简化`kubectl create -f`命令
```sh
k8screate a.yml b.yml
```

26. k8sapply: 简化`kubectl apply -f`命令
```sh
k8sapply a.yml b.yml
```

27. k8sdelete: 简化`kubectl delete -f`命令
```sh
k8sdelete a.yml b.yml
```

28. k8slabel: 切换是否显示标签，会改写配置文件`~/.kube/k8scmd.yml`, 用于控制全局各个资源列表的显示
```sh
k8slabel
```

29. k8soutput: 指定输出格式，会改写配置文件`~/.kube/k8scmd.yml`, 用于控制全局各个资源列表的显示
```sh
k8sdelete a.yml b.yml
```

## 全局配置 
配置文件`~/.kube/k8scmd.yml`, 用于控制全局各个资源列表的显示
```yaml
# 控制全局各个资源列表的显示
output-format: wide # 输出格式，如wide,yaml,json
show-labels: false # 显示标签
```
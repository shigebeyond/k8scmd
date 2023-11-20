[GitHub](https://github.com/shigebeyond/k8scmd) | [Gitee](https://gitee.com/shigebeyond/k8scmd)

# k8scmd - k8s命令精简版
## 概述
k8s命令很多，难记又难打，非常艰难；
我直接用python做了一个简化版的命令，易记又易打，非常简单；
同时对资源相关的命令，会自动填充资源的命名空间，不用用户操心也不用写。

- 目前仅支持linux环境，windows环境未测试

## 安装
```
pip install k8scmd
```

## 使用: 简化k8s命令
1. k8sstart/kstart: 启动 kubelet 服务
```
k8sstart
```

2. k8sstop/kstop: 停止 kubelet 服务
```
k8sstop
```

3. k8sall/kall: 查看所有资源
```sh
k8sall
```

4. k8sno/kno: 查删改 Node
```sh
# 查看所有Node资源列表
k8sno
k8sno -o yaml
# 查看单个Node资源详情
k8sno 资源名
k8sno 资源名 -o yaml
# 删除单个Node资源
k8sno 资源名 -d
# 编辑单个Node资源
k8sno 资源名 -e
# 过滤指定标签的Node资源列表，以下2个命令等价
k8sno @nginx
k8sno -l app=nginx
```

5. k8sns/kns: 查删改 Namespace
```sh
# 查看所有Namespace资源列表
k8sns
k8sns -o yaml
# 查看单个Namespace资源详情
k8sns 资源名
k8sns 资源名 -o yaml
# 删除单个Namespace资源
k8sns 资源名 -d
# 编辑单个Namespace资源
k8sns 资源名 -e
# 过滤指定标签的Namespace资源列表，以下2个命令等价
k8sns @nginx
k8sns -l app=nginx
```

6. k8spod/kpod: 查删改 Pod
```sh
# 查看所有Pod资源列表
k8spod
k8spod -o yaml
# 查看单个Pod资源详情
k8spod 资源名
k8spod 资源名 -o yaml
# 删除单个Pod资源
k8spod 资源名 -d
# 编辑单个Pod资源
k8spod 资源名 -e
# 过滤指定标签的Pod资源列表，以下2个命令等价
k8spod @nginx
k8spod -l app=nginx
```

7. k8ssvc/ksvc: 查删改 Service
```sh
# 查看所有Service资源列表
k8ssvc
k8ssvc -o yaml
# 查看单个Service资源详情
k8ssvc 资源名
k8ssvc 资源名 -o yaml
# 删除单个Service资源
k8ssvc 资源名 -d
# 编辑单个Service资源
k8ssvc 资源名 -e
# 过滤指定标签的Service资源列表，以下2个命令等价
k8ssvc @nginx
k8ssvc -l app=nginx
```

8. k8ssvcurl/ksvcurl: 查看所有Service的服务url+终端url，方便用户复制url
```sh
k8ssvcurl 
```
![](img/k8ssvcurl.png)

9. k8ssvccurl/ksvccurl: 对指定Service的服务url执行curl命令
```sh
k8ssvccurl 服务名
```
![](img/k8ssvccurl.png)

10. k8ssvcpod/ksvcpod: 查看Service的终端对应的pod
```sh
# 查看所有Service的终端对应的pod
k8ssvcpod
# 查看单个Service的终端对应的pod
k8ssvcpod 服务名
```
![](img/k8ssvcpod.png)

11. k8src/krc: 查删改 ReplicationController
```sh
# 查看所有ReplicationController资源列表
k8src
k8src -o yaml
# 查看单个ReplicationController资源详情
k8src 资源名
k8src 资源名 -o yaml
# 删除单个ReplicationController资源
k8src 资源名 -d
# 编辑单个ReplicationController资源
k8src 资源名 -e
# 过滤指定标签的ReplicationController资源列表，以下2个命令等价
k8src @nginx
k8src -l app=nginx
```

12. k8srs/krs: 查删改 ReplicaSet
```sh
# 查看所有ReplicaSet资源列表
k8srs
k8srs -o yaml
# 查看单个ReplicaSet资源详情
k8srs 资源名
k8srs 资源名 -o yaml
# 删除单个ReplicaSet资源
k8srs 资源名 -d
# 编辑单个ReplicaSet资源
k8srs 资源名 -e
# 过滤指定标签的ReplicaSet资源列表，以下2个命令等价
k8srs @nginx
k8srs -l app=nginx
```

13. k8sds/kds: 查删改 DaemonSet
```sh
# 查看所有DaemonSet资源列表
k8sds
k8sds -o yaml
# 查看单个DaemonSet资源详情
k8sds 资源名
k8sds 资源名 -o yaml
# 删除单个DaemonSet资源
k8sds 资源名 -d
# 编辑单个DaemonSet资源
k8sds 资源名 -e
# 过滤指定标签的DaemonSet资源列表，以下2个命令等价
k8sds @nginx
k8sds -l app=nginx

# 暂停 DaemonSet 的部署操作，等价于 kubectl rollout pause ds 资源名
k8sds 资源名 stop
# 恢复 DaemonSet 的部署操作，等价于 kubectl rollout resume ds 资源名
k8sds 资源名 start
# 重启 DaemonSet 的部署操作，即重启pod，等价于 kubectl rollout restart ds 资源名
k8sds 资源名 restart
```

14. k8ssts/ksts: 查删改 StatefulSet
```sh
# 查看所有StatefulSet资源列表
k8ssts
k8ssts -o yaml
# 查看单个StatefulSet资源详情
k8ssts 资源名
k8ssts 资源名 -o yaml
# 删除单个StatefulSet资源
k8ssts 资源名 -d
# 编辑单个StatefulSet资源
k8ssts 资源名 -e
# 过滤指定标签的StatefulSet资源列表，以下2个命令等价
k8ssts @nginx
k8ssts -l app=nginx

# 暂停 StatefulSet 的部署操作，等价于 kubectl rollout pause sts 资源名
k8ssts 资源名 stop
# 恢复 StatefulSet 的部署操作，等价于 kubectl rollout resume sts 资源名
k8ssts 资源名 start
# 重启 StatefulSet 的部署操作，即重启pod，等价于 kubectl rollout restart sts 资源名
k8ssts 资源名 restart
```

15. k8sdeploy/kdeploy: 查删改 Deployment
```sh
# 查看所有Deployment资源列表
k8sdeploy
k8sdeploy -o yaml
# 查看单个Deployment资源详情，等价于 kubectl describe deployment 资源名 + kubectl rollout status deployment 资源名
k8sdeploy 资源名
k8sdeploy 资源名 -o yaml
# 删除单个Deployment资源
k8sdeploy 资源名 -d
# 编辑单个Deployment资源
k8sdeploy 资源名 -e
# 过滤指定标签的Deployment资源列表，以下2个命令等价
k8sdeploy @nginx
k8sdeploy -l app=nginx

# 暂停 Deployment 的部署操作，等价于 kubectl rollout pause deploy 资源名
k8sdeploy 资源名 stop
# 恢复 Deployment 的部署操作，等价于 kubectl rollout resume deploy 资源名
k8sdeploy 资源名 start
# 重启 Deployment 的部署操作，即重启pod，等价于 kubectl rollout restart deploy 资源名
k8sdeploy 资源名 restart
```

16. k8shpa/khpa: 查删改 HorizontalPodAutoscaler
```sh
# 查看所有HorizontalPodAutoscaler资源列表
k8shpa
k8shpa -o yaml
# 查看单个HorizontalPodAutoscaler资源详情
k8shpa 资源名
k8shpa 资源名 -o yaml
# 删除单个HorizontalPodAutoscaler资源
k8shpa 资源名 -d
# 编辑单个HorizontalPodAutoscaler资源
k8shpa 资源名 -e
# 过滤指定标签的HorizontalPodAutoscaler资源列表，以下2个命令等价
k8shpa @nginx
k8shpa -l app=nginx
```

17. k8sconfig/kconfig: 查删改 ConfigMap
```sh
# 查看所有ConfigMap资源列表
k8sconfig
k8sconfig -o yaml
# 查看单个ConfigMap资源详情
k8sconfig 资源名
k8sconfig 资源名 -o yaml
# 删除单个ConfigMap资源
k8sconfig 资源名 -d
# 编辑单个ConfigMap资源
k8sconfig 资源名 -e
# 过滤指定标签的ConfigMap资源列表，以下2个命令等价
k8sconfig @nginx
k8sconfig -l app=nginx
```

18. k8ssecret/ksecret: 查删改 Secret
```sh
# 查看所有Secret资源列表
k8ssecret
k8ssecret -o yaml
# 查看单个Secret资源详情
k8ssecret 资源名
k8ssecret 资源名 -o yaml
# 删除单个Secret资源
k8ssecret 资源名 -d
# 编辑单个Secret资源
k8ssecret 资源名 -e
# 过滤指定标签的Secret资源列表，以下2个命令等价
k8ssecret @nginx
k8ssecret -l app=nginx
```

19. k8sendpoint/kendpoint: 查删改 Endpoint
```sh
# 查看所有Endpoint资源列表
k8sendpoint
k8sendpoint -o yaml
# 查看单个Endpoint资源详情
k8sendpoint 资源名
k8sendpoint 资源名 -o yaml
# 删除单个Endpoint资源
k8sendpoint 资源名 -d
# 编辑单个Endpoint资源
k8sendpoint 资源名 -e
# 过滤指定标签的Endpoint资源列表，以下2个命令等价
k8sendpoint @nginx
k8sendpoint -l app=nginx
```

20. k8sevent/kevent: 查删改 Event
```sh
# 查看所有Event资源列表
k8sevent
k8sevent -o yaml
# 查看单个Event资源详情
k8sevent 资源名
k8sevent 资源名 -o yaml
# 删除单个Event资源
k8sevent 资源名 -d
# 编辑单个Event资源
k8sevent 资源名 -e
# 过滤指定标签的Event资源列表，以下2个命令等价
k8sevent @nginx
k8sevent -l app=nginx
```

21. k8sjob/kjob: 查删改 Job
```sh
# 查看所有Job资源列表
k8sjob
k8sjob -o yaml
# 查看单个Job资源详情
k8sjob 资源名
k8sjob 资源名 -o yaml
# 删除单个Job资源
k8sjob 资源名 -d
# 编辑单个Job资源
k8sjob 资源名 -e
# 过滤指定标签的Job资源列表，以下2个命令等价
k8sjob @nginx
k8sjob -l app=nginx
```

22. k8scronjob/kcronjob: 查删改 Cronjob
```sh
# 查看所有Cronjob资源列表
k8scronjob
k8scronjob -o yaml
# 查看单个Cronjob资源详情
k8scronjob 资源名
k8scronjob 资源名 -o yaml
# 删除单个Cronjob资源
k8scronjob 资源名 -d
# 编辑单个Cronjob资源
k8scronjob 资源名 -e
# 过滤指定标签的Cronjob资源列表，以下2个命令等价
k8scronjob @nginx
k8scronjob -l app=nginx
```

23. k8sing/king: 查删改 Ingress
```sh
# 查看所有Ingress资源列表
k8sing
k8sing -o yaml
# 查看单个Ingress资源详情
k8sing 资源名
k8sing 资源名 -o yaml
# 删除单个Ingress资源
k8sing 资源名 -d
# 编辑单个Ingress资源
k8sing 资源名 -e
# 过滤指定标签的Ingress资源列表，以下2个命令等价
k8sing @nginx
k8sing -l app=nginx
```

24. k8singrule/kingrule: 查看所有Ingress资源的规则
```sh
k8singrule
```
![](img/k8singrule.png)


25. k8spv/kpv: 查删改 PersistentVolume
```sh
# 查看所有PersistentVolume资源列表
k8spv
k8spv -o yaml
# 查看单个PersistentVolume资源详情
k8spv 资源名
k8spv 资源名 -o yaml
# 删除单个PersistentVolume资源
k8spv 资源名 -d
# 编辑单个PersistentVolume资源
k8spv 资源名 -e
# 过滤指定标签的PersistentVolume资源列表，以下2个命令等价
k8spv @nginx
k8spv -l app=nginx
```

26. k8spvc/kpvc: 查删改 PersistentVolumeClaim
```sh
# 查看所有PersistentVolumeClaim资源列表
k8spvc
k8spvc -o yaml
# 查看单个PersistentVolumeClaim资源详情
k8spvc 资源名
k8spvc 资源名 -o yaml
# 删除单个PersistentVolumeClaim资源
k8spvc 资源名 -d
# 编辑单个PersistentVolumeClaim资源
k8spvc 资源名 -e
# 过滤指定标签的PersistentVolumeClaim资源列表，以下2个命令等价
k8spvc @nginx
k8spvc -l app=nginx
```

27. k8ssc/ksc: 查删改 StorageClass
```sh
# 查看所有StorageClass资源列表
k8ssc
k8ssc -o yaml
# 查看单个StorageClass资源详情
k8ssc 资源名
k8ssc 资源名 -o yaml
# 删除单个StorageClass资源
k8ssc 资源名 -d
# 编辑单个StorageClass资源
k8ssc 资源名 -e
# 过滤指定标签的StorageClass资源列表，以下2个命令等价
k8ssc @nginx
k8ssc -l app=nginx
```

28. k8saccount/kaccount: 查删改 ServiceAccount
```sh
# 查看所有ServiceAccount资源列表
k8saccount
k8saccount -o yaml
# 查看单个ServiceAccount资源详情
k8saccount 资源名
k8saccount 资源名 -o yaml
# 删除单个ServiceAccount资源
k8saccount 资源名 -d
# 编辑单个ServiceAccount资源
k8saccount 资源名 -e
# 过滤指定标签的ServiceAccount资源列表，以下2个命令等价
k8saccount @nginx
k8saccount -l app=nginx
```

29. k8srole/krole: 查删改 Role
```sh
# 查看所有Role资源列表
k8srole
k8srole -o yaml
# 查看单个Role资源详情
k8srole 资源名
k8srole 资源名 -o yaml
# 删除单个Role资源
k8srole 资源名 -d
# 编辑单个Role资源
k8srole 资源名 -e
# 过滤指定标签的Role资源列表，以下2个命令等价
k8srole @nginx
k8srole -l app=nginx
```

30. k8srolebind/krolebind: 查删改 RoleBinding
```sh
# 查看所有RoleBinding资源列表
k8srolebind
k8srolebind -o yaml
# 查看单个RoleBinding资源详情
k8srolebind 资源名
k8srolebind 资源名 -o yaml
# 删除单个RoleBinding资源
k8srolebind 资源名 -d
# 编辑单个RoleBinding资源
k8srolebind 资源名 -e
# 过滤指定标签的RoleBinding资源列表，以下2个命令等价
k8srolebind @nginx
k8srolebind -l app=nginx
```

31. k8scrole/kcrole: 查删改 ClusterRole
```sh
# 查看所有ClusterRole资源列表
k8scrole
k8scrole -o yaml
# 查看单个ClusterRole资源详情
k8scrole 资源名
k8scrole 资源名 -o yaml
# 删除单个ClusterRole资源
k8scrole 资源名 -d
# 编辑单个ClusterRole资源
k8scrole 资源名 -e
# 过滤指定标签的ClusterRole资源列表，以下2个命令等价
k8scrole @nginx
k8scrole -l app=nginx
```

32. k8scrolebind/kcrolebind: 查删改 ClusterRoleBinding
```sh
# 查看所有ClusterRoleBinding资源列表
k8scrolebind
k8scrolebind -o yaml
# 查看单个ClusterRoleBinding资源详情
k8scrolebind 资源名
k8scrolebind 资源名 -o yaml
# 删除单个ClusterRoleBinding资源
k8scrolebind 资源名 -d
# 编辑单个ClusterRoleBinding资源
k8scrolebind 资源名 -e
# 过滤指定标签的ClusterRoleBinding资源列表，以下2个命令等价
k8scrolebind @nginx
k8scrolebind -l app=nginx
```

33. k8sexec/kexec: 在pod中执行命令
```sh
k8sexec Pod资源名 命令
# 例如
k8sexec nginx ls -l
```

34. k8sbash/kbash: 进入pod bash
```sh
k8sbash Pod资源名
k8sbash Pod资源名:容器名
# 例如
k8sbash nginx
```

35. k8ssh/ksh: 进入pod sh
```sh
k8ssh Pod资源名
k8ssh Pod资源名:容器名
# 例如
k8ssh nginx
```

36. k8slog/klog: 查看pod日志
```sh
k8slog Pod资源名 [-f]
# 例如
k8slog nginx
k8slog nginx -f
```

37. k8sletlog/kletlog: 查看kubelet服务日志
```sh
k8sletlog
k8sletlog -f
```

38. k8screate/kcreate: 简化`kubectl create -f`命令
```sh
k8screate a.yml b.yml
```

39. k8sapply/kapply: 简化`kubectl apply -f`命令
```sh
k8sapply a.yml b.yml
```

40. k8sdelete/kdelete: 简化`kubectl delete -f`命令
```sh
k8sdelete a.yml b.yml
```

41. k8sdiff/kdiff: 简化`kubectl diff -f`命令
```sh
k8sdiff a.yml b.yml
```

42. k8sscale/kscale: 扩容
```sh
k8sscale Deployment资源名 副本数
```

43. k8shistory/khistory: 查看 Deployment 历史记录
```sh
# 查看所有历史版本
k8shistory Deployment资源名
# 查看单个版本详情
k8shistory Deployment资源名 版本号
```

44. k8srollback/krollback: 查看 Deployment 历史记录
```sh
# 回滚到上一个版本
k8srollback Deployment资源名
# 回滚到指定版本
k8srollback Deployment资源名 版本号
```

45. k8sgetlabels/kgetlabels: 切换是否显示标签，会改写配置文件`~/.kube/k8scmd.yml`, 用于控制全局各个资源列表(即kubectl get命令)的显示
```sh
k8sgetlabels
```

46. k8sgetoutput/kgetoutput: 指定输出格式，会改写配置文件`~/.kube/k8scmd.yml`, 用于控制全局各个资源列表(即kubectl get命令)的显示
```sh
# 指定输出格式
k8sgetoutput yaml
# 无指定输出格式，则在wide,yaml之间切换
k8sgetoutput
```

47. k8sgetns/kgetns: 指定过滤的命名空间，会改写配置文件`~/.kube/k8scmd.yml`, 用于控制全局各个资源列表(即kubectl get命令)的显示
```sh
# 指定过滤的命名空间
k8sgetns yaml
# 无指定过滤的命名空间，则为全部命名空间
k8sgetns
```

48. k8sapi/kapi: 查看api资源文档
```sh
# 查看所有api资源
k8sapi
# 查看资源或字段的文档
k8sapi 资源或字段
# 如 
k8sapi pod
k8sapi pods.spec.containers
```

49. k8sbuild/kbuild: 替代`docker build`命令，用于构建docker镜像，并将镜像导入containerd的k8s命名空间中
```sh
k8sbuild -t rpcserver .
kbuild -t 192.168.0.182:5000/rpcserver:3.0.0 .
```

## 使用: 精简Argo Workflows命令
参考 [argo-cmd](argo-cmd.md)

## 全局配置 
配置文件`~/.kube/k8scmd.yml`, 用于控制全局各个资源列表(即kubectl get命令)的显示
```yaml
# 控制全局各个资源列表的显示
get-output: wide # 输出格式，如wide,yaml,json
get-labels: false # 显示标签
get-ns:  # 命名空间
```

## 简化argo命令(/usr/local/bin/argo)
1. wf: 查删改 Workflow
```sh
# 查看所有Workflow资源列表
wf
wf -o yaml
# 查看单个Workflow资源详情
wf 资源名
wf 资源名 -o yaml
# 删除单个Workflow资源
wf 资源名 -d
# 过滤指定标签的Workflow资源列表，以下2个命令等价
wf @nginx
wf -l app=nginx
```

2. wfsubmit: 提交 Workflow
```
wfsubmit 资源文件
```

3. wfclear: 删除所有 Workflow
```
wfclear
```

4. wflog: 查看指定 Workflow 的日志
```
wflog 流程名
# 查看最新流程的日志，下面2个命令等价
wflog @latest
wflog
```

5. wfretry: 重试指定 Workflow
```
wfretry 流程名
# 重试最新流程，下面2个命令等价
wfretry @latest
wfretry
```

6. wfsuspend: 暂停指定 Workflow 
```
wfsuspend 流程名
# 暂停最新流程，下面2个命令等价
wfsuspend @latest
wfsuspend
```

7. wfresume: 恢复 Workflow 
```
wfresume 流程名
# 恢复最新流程，下面2个命令等价
wfresume @latest
wfresume
```

8. cwf: 查删改 CronWorkflow
```sh
# 查看所有CronWorkflow资源列表
cwf
cwf -o yaml
# 查看单个CronWorkflow资源详情
cwf 资源名
cwf 资源名 -o yaml
# 删除单个CronWorkflow资源
cwf 资源名 -d
# 过滤指定标签的CronWorkflow资源列表，以下2个命令等价
cwf @nginx
cwf -l app=nginx
```

9. cwfcreate: 创建 CronWorkflow
```
cwfcreate 资源文件
```

10. cwfsuspend: 暂停指定 CronWorkflow 
```
cwfsuspend 定时流程名
# 暂停最新流程，下面2个命令等价
cwfsuspend @latest
cwfsuspend
```

11. cwfresume: 恢复 CronWorkflow 
```
cwfresume 定时流程名
# 恢复最新流程，下面2个命令等价
cwfresume @latest
cwfresume
```

12. wft: 查删改 WorkflowTemplate
```sh
# 查看所有WorkflowTemplate资源列表
wft
wft -o yaml
# 查看单个WorkflowTemplate资源详情
wft 资源名
wft 资源名 -o yaml
# 删除单个WorkflowTemplate资源
wft 资源名 -d
# 过滤指定标签的WorkflowTemplate资源列表，以下2个命令等价
wft @nginx
wft -l app=nginx
```

13. wftcreate: 创建 WorkflowTemplate
```
wftcreate 资源文件
```

14. cwft: 查删改 ClusterWorkflowTemplate
```sh
# 查看所有ClusterWorkflowTemplate资源列表
cwft
cwft -o yaml
# 查看单个ClusterWorkflowTemplate资源详情
cwft 资源名
cwft 资源名 -o yaml
# 删除单个ClusterWorkflowTemplate资源
cwft 资源名 -d
# 过滤指定标签的ClusterWorkflowTemplate资源列表，以下2个命令等价
cwft @nginx
cwft -l app=nginx
```

15. cwftcreate: 创建 ClusterWorkflowTemplate
```
cwftcreate 资源文件
```


## 简化Argo Workflows相关的k8s资源管理命令(/usr/bin/kubectl)
1. k8swf/kwf: 查删改 Argo Workflow
```sh
# 查看所有Argo Workflow资源列表
k8swf
k8swf -o yaml
# 查看单个Argo Workflow资源详情
k8swf 资源名
k8swf 资源名 -o yaml
# 删除单个Argo Workflow资源
k8swf 资源名 -d
# 编辑单个Argo Workflow资源
k8swf 资源名 -e
# 过滤指定标签的Argo Workflow资源列表，以下2个命令等价
k8swf @nginx
k8swf -l app=nginx
```

2. k8swft/kwft: 查删改 Argo WorkflowTemplate
```sh
# 查看所有Argo WorkflowTemplate资源列表
k8swft
k8swft -o yaml
# 查看单个Argo WorkflowTemplate资源详情
k8swft 资源名
k8swft 资源名 -o yaml
# 删除单个Argo WorkflowTemplate资源
k8swft 资源名 -d
# 编辑单个Argo WorkflowTemplate资源
k8swft 资源名 -e
# 过滤指定标签的Argo WorkflowTemplate资源列表，以下2个命令等价
k8swft @nginx
k8swft -l app=nginx
```

3. k8scwft/kcwft: 查删改 Argo ClusterWorkflowTemplate
```sh
# 查看所有Argo ClusterWorkflowTemplate资源列表
k8scwft
k8scwft -o yaml
# 查看单个Argo ClusterWorkflowTemplate资源详情
k8scwft 资源名
k8scwft 资源名 -o yaml
# 删除单个Argo ClusterWorkflowTemplate资源
k8scwft 资源名 -d
# 编辑单个Argo ClusterWorkflowTemplate资源
k8scwft 资源名 -e
# 过滤指定标签的Argo ClusterWorkflowTemplate资源列表，以下2个命令等价
k8scwft @nginx
k8scwft -l app=nginx
```

4. k8scwf/kcwf: 查删改 Argo CronWorkflow
```sh
# 查看所有Argo CronWorkflow资源列表
k8scwf
k8scwf -o yaml
# 查看单个Argo CronWorkflow资源详情
k8scwf 资源名
k8scwf 资源名 -o yaml
# 删除单个Argo CronWorkflow资源
k8scwf 资源名 -d
# 编辑单个Argo CronWorkflow资源
k8scwf 资源名 -e
# 过滤指定标签的Argo CronWorkflow资源列表，以下2个命令等价
k8scwf @nginx
k8scwf -l app=nginx
```

5. k8swfevent/kwfevent: 查删改 Argo WorkflowEventBinding
```sh
# 查看所有Argo WorkflowEventBinding资源列表
k8swfevent
k8swfevent -o yaml
# 查看单个Argo WorkflowEventBinding资源详情
k8swfevent 资源名
k8swfevent 资源名 -o yaml
# 删除单个Argo WorkflowEventBinding资源
k8swfevent 资源名 -d
# 编辑单个Argo WorkflowEventBinding资源
k8swfevent 资源名 -e
# 过滤指定标签的Argo WorkflowEventBinding资源列表，以下2个命令等价
k8swfevent @nginx
k8swfevent -l app=nginx
```
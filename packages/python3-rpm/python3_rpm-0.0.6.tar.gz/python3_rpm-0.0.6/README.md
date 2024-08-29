# python3-rpm
## 安装
```bash
pip3 install python3-rpm
```

## 设置变量
修改 [env.sh](env.sh) 中变量的值，然后执行如下命令使变量生效
```bash
source env.sh
```



## 用法
### rpm_ai 命令用法
* 获取指定软件包的所有服务
```bash
rpm_ai rpm get_service httpd
```

* 获取指定软件包的命令参数列表
```bash
rpm_ai rpm get_cmd_and_param acl
```

### rpm 库用法
获取软件包提供的服务列表
```python
from rpm.rpm import RpmService

rpm=RpmService()
service_list=rpm.get_service("mysql-server")
print(service_list)
```
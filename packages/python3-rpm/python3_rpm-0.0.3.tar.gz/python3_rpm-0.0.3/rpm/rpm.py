import re
import os
from log import log
from ssh.ssh import SSHClient
from chatgpt.chatgpt import ChatGPT


class RpmService():
    def get_service(self, rpm_name):
        log.info(f"begin to get service list for {rpm_name}...")
        ssh = SSHClient(ip=os.environ.get("SERVER_IP", "127.0.0.1"), port=os.environ.get("SERVER_PORT", 22),
                        username=os.environ.get("SERVER_USERNAME", "root"),
                        password=os.environ.get("SERVER_PASSWORD", "root@123"))
        ssh.exec(f"dnf install -y {rpm_name}", timeout=1200)
        output = ssh.exec("rpm -ql " + rpm_name + " | grep -E 'service$'|grep -v @|awk -F / '{print $NF}'",
                          timeout=20).stdout.strip()
        service_list = [elem.strip() for elem in output.split("\n")]
        log.info(f"total {len(service_list)} service list. They are:")
        return service_list

    def get_sub_command_list(self, command):
        chatgpt = ChatGPT(base_url=os.environ("OPENAI_BASE_URL"),api_key=os.environ("OPENAI_API_KEY"))
        sub_commands = []
        question = f"请列出 {command} 命令的子命令列表，只需要列出子命令列表，无需其他任何多余的解释，如果没有子命令，则直接返回空字符串"
        rs = chatgpt.ask(question)
        rs = rs.strip().replace("-", "").strip()
        for elem in rs.split("\n"):
            temp = re.search("([a-zA-Z]+)", elem)
            if temp:
                sub_command = temp.group(1)
                if sub_command != command:
                    sub_commands.append(temp.group(1))
        return sub_commands

    def get_param_list(self,cmd):
        ssh = SSHClient(ip=os.environ.get("SERVER_IP", "127.0.0.1"), port=os.environ.get("SERVER_PORT", 22),
                        username=os.environ.get("SERVER_USERNAME", "root"),
                        password=os.environ.get("SERVER_PASSWORD", "root@123"))
        params = []
        output = ssh.exec(
                cmd + " --help 2>&1 |grep -Ei '^\s*-[a-zA-Z]'|awk -F ' ' '{print $1}'|awk -F ',' '{print $1}' \n\n",
                timeout=60).stdout.strip()
        if len(output) >= 0:
            for line in output.split("\n"):
                if line.startswith("-"):
                    params.append(line.strip())
        output = ssh.exec(
                cmd + " --help 2>&1 |grep -E '^\s*--[a-zA-Z\=_-]*\s'|awk -F ' ' '{print $1}'|awk -F '=' '{print $1}'' \n\n",
                timeout=30).stdout.strip()
        if len(output) > 0:
            for line in output.split("\n"):
                if line.startswith("--"):
                    params.append(line.strip())
        output = ssh.exec(
            cmd + " --help 2>&1 |grep -E '^\s*-[a-zA-Z0-9],\s*--[a-zA-Z1-9\=_-]*\s'|awk -F ',' '{print $2}' |awk -F ' ' '{print $1}' \n\n",
            timeout=10).output.strip()
        if len(output) > 0:
            for line in output.split("\n"):
                if line.startswith("--"):
                    params.append(line.strip())
        return params


    def get_cmd_and_param(self, rpm_name):
        log.info(f"begin to get cmd and param for {rpm_name}...")
        ssh = SSHClient(ip=os.environ.get("SERVER_IP", "127.0.0.1"), port=os.environ.get("SERVER_PORT", 22),
                        username=os.environ.get("SERVER_USERNAME", "root"),
                        password=os.environ.get("SERVER_PASSWORD", "root@123"))
        ssh.exec(f"dnf install -y {rpm_name}", timeout=1200)
        output = ssh.exec("rpm -ql " + rpm_name + " | grep /usr/bin | awk -F'/' '{print $NF}'",
                          timeout=10).stdout.strip()
        cmds = [line.strip() for line in output.split("\n") if line.strip()]
        cmds_list = []
        for cmd in cmds:
            sub_commands = self.get_sub_command_list(cmd)
            for sub_command in sub_commands:
                if sub_command and sub_command != cmd:
                    new_command = f"{cmd} {sub_command}"
                else:
                    new_command = cmd
                if new_command not in cmds_list:
                    cmds_list.append(new_command)
        cmd_params_list=[]
        for cmd in cmds_list:
            params = self.get_param_list(cmd)
            for param in params:
                tmp={
                    "cmd":cmd,
                    "param":param
                }
                cmd_params_list.append(tmp)
        return cmd_params_list



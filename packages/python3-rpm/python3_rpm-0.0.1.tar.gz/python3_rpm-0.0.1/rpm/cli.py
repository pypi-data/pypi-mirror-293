import fire
from log import log
from rpm.ssh import SSHClient
from rpm.config import config

class RPM():

    def get_service(self,rpm_name):
        log.info(f"begin to get service list for {rpm_name}...")
        ssh=SSHClient(ip=config.server_ip,port=config.server_port,username=config.username,password=config.password)
        ssh.exec(f"dnf install -y {rpm_name}",timeout=120)
        output = ssh.exec("rpm -ql " + rpm_name + " | grep -E 'service$'|grep -v @|awk -F / '{print $NF}'",
                          timeout=20).output.strip()
        service_list = [elem.strip() for elem in output.split("\n")]
        log.info(f"total {len(service_list)} service list. They are:")
        for service in service_list:
            print(service)


def main():
    fire.Fire(
        {
            "rpm": RPM
        }
    )

if __name__=="__main__":
    main()
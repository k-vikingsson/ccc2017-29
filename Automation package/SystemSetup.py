##
## COMP90024 Cluster and Cloud Computing
## Assignment 2
## City: Melbourne
##
## File: SystemSetup.py
## Description: Python script to run automation.
##
## Team 29
## Members:
## Name         | Student ID | e-mail
## Hangyu XIA   | 802971     | hangyux@student.unimelb.edu.au
## Hanwei ZHU   | 811443     | hanweiz@student.unimelb.edu.au
## Jinchao CAI  | 838073     | jinchaoc1@student.unimelb.edu.au
## Wenzhuo MI   | 818944     | miw@student.unimelb.edu.au
## Zequn MA     | 696586     | zequnm@dimefox.eng.unimelb.edu.au
##

import os
import sys
import boto
import time
import argparse
import configparser
from boto.ec2.keypair import KeyPair
from boto.exception import BotoClientError
from boto.ec2.regioninfo import RegionInfo


class SystemSetup(object):
    """SystemSetup is class that will add and run instances in nectar, prepare the environment for system at each node automatically"""

    def __init__(self, endpoint='nova.rc.nectar.org.au', name='melbourne'):
        super(SystemSetup, self).__init__()
        self.image_id = 'ami-86f4a44c'
        # self.endpoint = endpoint
        # self.name = name

    def read_config(self, arg):
        f_option_help_message = '''configuartion file, below is a template
        [config]\n
        admin = [admin]\n
        password = [password]\n
        key_name = [key_name]\n
        node_number = [node_number]\n
        instance_type = [instace_type]\n
        python_script = [python_script]
        aws_access_key_id = [aws_access_key_id]\n
        aws_secret_access_key = [aws_secret_access_key]\n'''
        arg_parser = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter, description=f_option_help_message)
        arg_parser.add_argument(
            '-f', required=True, help='path of configuration file')
        args = vars(arg_parser.parse_args(arg))
        config_parser = configparser.ConfigParser()
        config_parser.read(args['f'])
        self.admin = config_parser.get('config', 'admin')
        self.password = config_parser.get('config', 'password')
        self.key_name = config_parser.get('config', 'key_name')
        self.python_script = config_parser.get('config', 'python_script')
        self.node_number = config_parser.get('config', 'node_number')
        self.instance_type = config_parser.get('config', 'instance_type')
        self.aws_access_key_id = config_parser.get(
            'config', 'aws_access_key_id')
        self.aws_secret_access_key = config_parser.get(
            'config', 'aws_secret_access_key')
        if os.path.exists(self.python_script):
            pass
        else:
            print('python_script does not exist')
            sys.exit(0)

    def run_instances(self):
        region = RegionInfo(name='melbourne', endpoint='nova.rc.nectar.org.au')
        ec2_conn = boto.connect_ec2(self.aws_access_key_id, self.aws_secret_access_key, is_secure=True,
                                    region=region, port=8773, path='/services/Cloud', validate_certs=False)
        # key_pair_list = ec2_conn.get_all_key_pairs()
        # key_name_existed = False
        # for key_pair in key_pair_list:
        #     if key_pair.name == self.key_name:
        #         key_name_existed = True
        # if not key_name_existed:
        key_pair = ec2_conn.create_key_pair(self.key_name)
        # else:
        #     key_pair = ec2_conn.get_key_pair(self.key_name)
        self.save_key_pair(key_pair, './')
        reservation = ec2_conn.run_instances(
            image_id='ami-86f4a44c', min_count=self.node_number, max_count=self.node_number, security_groups=['ssh', 'default', 'http', 'icmp'], key_name=self.key_name, instance_type=self.instance_type)
        self.nodes_ip = []
        self.instances_id = []
        for instance in reservation.instances:
            self.instances_id.append(instance.id)
        print(self.instances_id)
        # time.sleep(30)
        ec2_conn = boto.connect_ec2(self.aws_access_key_id, self.aws_secret_access_key, is_secure=True,
                                    region=region, port=8773, path='/services/Cloud', validate_certs=False)
        while True:
            reservations = ec2_conn.get_all_instances()
            flag = True
            self.nodes_ip = []
            for reservation in reservations:
                for instance in reservation.instances:
                    if instance.id in self.instances_id:
                        if instance.private_ip_address == '':
                            flag = False
                        else:
                            self.nodes_ip.append(instance.private_ip_address)
            if flag:
                break

    def setup_environment(self):
        with open('hosts', 'w') as f:
            f.write('[default]\n')
            for ip in self.nodes_ip:
                f.write(ip + '\n')
            f.write('[default:vars]\n')
            f.write('master = ' + self.nodes_ip[0] + '\n')
            f.write('admin = ' + self.admin + '\n')
            f.write('password = ' + self.password + '\n')
            f.write('python_script = ' + self.python_script + '\n')
            f.close()
        command = 'ansible-playbook -i hosts --private-key=' + \
            self.key_name + '.pem' + ' --timeout=30' + ' setup.yaml'
        os.system(command)

    def rollback(self):
        region = RegionInfo(name='melbourne', endpoint='nova.rc.nectar.org.au')
        ec2_conn = boto.connect_ec2(self.aws_access_key_id, self.aws_secret_access_key, is_secure=True,
                                    region=region, port=8773, path='/services/Cloud', validate_certs=False)
        key_pair_list = ec2_conn.get_all_key_pairs()
        key_name_existed = False
        for key_pair in key_pair_list:
            if key_pair.name == self.key_name:
                key_name_existed = True
        if not key_name_existed:
            ec2_conn.delete_key_pair(self.key_name)
        reservations = ec2_conn.get_all_instances()
        for reservation in reservations:
            for instance in reservation.instances:
                if instance.id in self.instances_id:
                    ec2_conn.terminate_instances(instance.id)

    def save_key_pair(self, key_pair, directory_path):
        # print(key_pair.material)
        if key_pair.material:
            directory_path = os.path.expanduser(directory_path)
            file_path = os.path.join(directory_path, '%s.pem' % key_pair.name)
            # if os.path.exists(file_path):
            #     raise BotoClientError(
            #         '%s already exists, it will not be overwritten' % file_path)
            fp = open(file_path, 'w')
            fp.write(key_pair.material)
            fp.close()
            os.chmod(file_path, 0o600)
            return True
        else:
            raise BotoClientError('KeyPair contains no material')
        pass

if __name__ == '__main__':
    try:
        system_setup = SystemSetup()
        system_setup.read_config(sys.argv[1:])
        system_setup.run_instances()
        system_setup.setup_environment()
        print(system_setup.nodes_ip)
    except Exception as e:
        system_setup.rollback()
        raise e

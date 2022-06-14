# @Author: Southseast
# @Date: 2022-06-13 17:28
import argparse
import os
import subprocess
from shutil import copyfile


class ZendDecode:

    def __init__(self, prefix_path, source_path, target_path):
        self.decode_type = ""
        self.source_path = source_path
        self.target_path = target_path
        self.config = {
            "52RM": {"exec_path": prefix_path + "lib/52RM/php.exe",
                     "arg": "\"%s\" /tab /indent:1 /path:\"%s\" /ext:.php /noexpire"},
            "52NM": {"exec_path": prefix_path + "lib/52NM/php.exe",
                     "arg": "\"%s\" /tab /indent:1 /path:\"%s\" /ext:.php /noexpire"},
            "53": {"exec_path": prefix_path + "lib/53/php.exe",
                   "arg": prefix_path + "lib/53/phpdc.phpr %s > %s"},
            "54": {"exec_path": prefix_path + "lib/54/php.exe",
                   "arg": prefix_path + "lib/54/phpdc.phpr %s > %s"},
        }
        self.suffix = ".php"

    def write_file(self, file_path, target_path):
        exec_path = self.config[self.decode_type]["exec_path"]
        arg = self.config[self.decode_type]["arg"]
        command = exec_path + " " + (arg % (file_path, target_path))
        try:
            code, output = subprocess.getstatusoutput(command)
            print(output, target_path)
        except:
            return

    def check_zend(self, path):
        if not path.endswith(self.suffix):
            return False
        f = open(path, "rb").read()
        if b"<?php @Zend;" in f or b"Zend\x00" in f:
            return True
        else:
            return False

    def traverse(self):
        for i in self.find_all_file():
            target_path = i.replace(self.source_path, self.target_path)
            target_dir = os.path.dirname(target_path)
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)
            if self.check_zend(i):
                if "52" in self.decode_type:
                    self.write_file(i, target_dir)
                else:
                    self.write_file(i, target_path)
            else:
                copyfile(i, target_path)

    def check_arg(self, decode_type):
        if decode_type in self.config:
            self.decode_type = decode_type
            return True
        else:
            print("arg err")
            return False

    def find_all_file(self):
        for root_name, middle_name_list, file_name_list in os.walk(self.source_path):
            for file_name in file_name_list:
                fullname = os.path.join(root_name, file_name)
                yield fullname


if __name__ == '__main__':
    prefix_path = os.getcwd() + "/"
    parser = argparse.ArgumentParser(description='ZendDecode')
    parser.add_argument('--source_path', '-s', help='源码读取路径，若无指定则读取source', default=prefix_path + "source/")
    parser.add_argument('--target_path', '-t', help='解码保存路径，若无指定则输出到target', default=prefix_path + "target/")
    parser.add_argument('--decode_type', '-d', help='解码格式，必要参数，可选为52RM/52NM/53/54', required=True)
    args = parser.parse_args()
    zd = ZendDecode(prefix_path, args.source_path, args.target_path)
    if zd.check_arg(args.decode_type):
        zd.traverse()

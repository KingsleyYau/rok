from ppadb.client import Client as PPADBClient
from utils import resource_path
from utils import build_command
from utils import log
from filepath.tool_relative_paths import FilePaths
import subprocess
import traceback

bridge = None


class Adb:

    def __init__(self, host='127.0.0.1', port=5037):
        self.client = PPADBClient(host, port)

    def connect_to_device(self, host='127.0.0.1', port=5555):
        adb_path = resource_path(FilePaths.ADB_EXE_PATH.value)
        cmd = build_command(adb_path, 'connect', "{}:{}".format(host, port))
        ret = subprocess.check_output(cmd, shell=True, stderr=subprocess.PIPE, encoding="utf-8", timeout=2)
        log('connect_to_device', ret)

    def get_client_devices(self):
        return self.client.devices()

    def get_device(self, host='127.0.0.1', port=5555):
        log('get_device', host, port)
        try:
            self.client.remote_connect(host, port)
            device = self.client.device('{}:{}'.format(host, port))
            device.host = host
            device.port = port
            log('get_device', host, port, device)
        except Exception as e:
            traceback.print_exc()
            enable_adb()
            return None
        return device
    
    def reconnect(self, device):
        try:
            host = device.host
            port = device.port
            log('reconnect', host, port)
            self.connect_to_device(host, port)
            self.client.remote_connect(host, port)
            device = self.client.device('{}:{}'.format(host, port))
            log('reconnect', '[OK]', host, port, device)
        except Exception as e:
            log('reconnect', '[ERR]', host, port, e)
            traceback.print_exc()
            enable_adb()
            return None
        return device

def enable_adb(host='127.0.0.1', port=5037):
    adb = None
    adb_path = resource_path(FilePaths.ADB_EXE_PATH.value)
    log('enable_adb', adb_path, host, port)
    try:
        adb = Adb(host, port)

        version = adb.client.version()

        if version != 41:
            raise RuntimeError('Error: require adb version 41, but version is {}'.format(version))
        adb.client.devices()
        
    except RuntimeError as err:
        log('enable_adb', err)
        cmd = build_command(adb_path + ' kill-server')
        ret = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
        log('enable_adb', cmd, ret)
        cmd = build_command(adb_path + ' start-server')
        ret = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
        log('enable_adb', cmd, ret)
        #
        # if ret.returncode != 0:
        #     raise RuntimeError('Error: fail to start adb server. \n({})'.format(ret))

    return adb

import adb

from gui.main_window import MainWindow
import argparse
from api.api import run_api

def str2bool(v):
    if v.lower() in ('yes', 'true', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Unsupported value encountered.')
    
def main():
    # adb.bridge = adb.enable_adb('192.168.88.140', 9037)
    adb.bridge = adb.enable_adb('127.0.0.1', 5037)
    window = MainWindow()
    window.run()
    
def api(args):
    run_api(args)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--api", type=str2bool, default=False, help="api mode")
    parser.add_argument("--run_type", type=str, default='request_title', help="run_type")
    parser.add_argument("--device_name", type=str, default='request_title', help="device_name")
    parser.add_argument("--run", type=str2bool, default=True, help="start/stop bot")
    parser.add_argument("--title", type=str, default='train', help="title")
    parser.add_argument("--server", type=str, default='15', help="title")
    parser.add_argument("--x", type=str, default='0', help="x")
    parser.add_argument("--y", type=str, default='0', help="y")
    parser.add_argument("--player", type=int, default='1', help="player")
    args = parser.parse_args()
    if args.api:
        api(args)
    else:
        main()

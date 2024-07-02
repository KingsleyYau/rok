import adb

from gui.main_window import MainWindow
import argparse
from api.api import run_api, get_bot, monitor
from utils import log
from api.run_config import RunConfig

from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib
import json
import time

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

def api_monitor(args):
    bot = get_bot(args.device_name)
    args.run_type = 'request_monitor'
    while True:
        run_api(args, bot)
        # time.sleep(2)
    
def api_deamon(args):
    bot = get_bot()
    filepath = args.api_deamon_file
    filepath_last = args.api_deamon_file_last
    while True:
        # 读取上次使用记录
        last_item = None
        try:
            with open(filepath_last, 'r', encoding='utf-8') as lf:
                line = lf.readline()
                last_item = json.loads(line)
        except BaseException as e:
            log(e) 
            
        # 读取当前队列记录       
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                if len(lines) > 0:
                    item = None
                    result = False
                    playe_name = ""
                    try:
                        line = lines[0]
                        item = json.loads(line)
                        log('################################################################################')
                        log('执行记录', item)
                        record = item['record']
                        
                        if last_item is not None:
                            last_record = last_item['record']
                            assign_time = last_item['assign_time']
                            dt = time.strptime(assign_time, "%Y-%m-%d %H:%M:%S")
                            last = time.mktime(dt)
                            if record['title'] == last_record['title']:
                                while True:
                                    now = time.time()
                                    diff = now - last
                                    if diff < 60:
                                        title_item = RunConfig.TITLE_ITEMS[last_record['title']]
                                        if title_item is not None:
                                            log('等待玩家使用', title_item['name'], '上次发放时间', assign_time, '当前执行时间', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), '使用时长', int(diff))
                                            time.sleep(10)
                                        else:
                                            break
                                    else:
                                        break
                        
                        # 执行记录
                        args.run_type = 'request_title'
                        args.title = record['title']
                        args.server = record['server']
                        args.x = record['x']
                        args.y = record['y']
                        result, playe_name = run_api(args, bot)
                    except BaseException as e:
                        log(item, e)
                        adb.bridge.reconnect(bot.device)
                    
                    try:    
                        # 移除记录
                        with open(filepath, 'r+', encoding='utf-8') as nf:
                            lines = nf.readlines()
                            lines = lines[1:]
                            nf.seek(0)
                            nf.truncate()
                            nf.writelines(lines)
                    except BaseException as e:
                        log(item, e)
                    
                    try:        
                        if item is not None and result:
                            with open(filepath_last, 'w', encoding='utf-8') as wf:
                                record = item['record']
                                item['assign_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                                item['player_name'] = playe_name
                                line = json.dumps(item, ensure_ascii=False)
                                wf.writelines([line])
                                wf.truncate()
                            # # 发放成功, 等待使用
                            # time.sleep(40)
                    except BaseException as e:
                        log(item, e)  
                              
        except BaseException as e:
            log(e)
        time.sleep(3)
        
def api(args):
    run_api(args)

class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        pr = urllib.parse.urlparse(self.path)
        self._response(self.path, pr)

    def do_POST(self):
        pr = urllib.parse.urlparse(self.path)
        self._response(self.path, pr)
   
    def _response(self, path, pr):
        rp = {
            'errno':0,
            'errmsg':"",
        }
        if pr:
            args = urllib.parse.parse_qs(pr.query)
            print(pr.path, args)
            query = {k: v[0] for k, v in args.items()}
            query_json = json.dumps(query, ensure_ascii=False)
            print(pr.path, query_json)
            
        self.send_response(200)
        self.send_header('Content-type', 'text/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        rp = json.dumps(rp, ensure_ascii=False)
        print(pr.path, rp)
        self.wfile.write(rp.encode())

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
    parser.add_argument("--api_deamon", type=str2bool, default=False, help="api deamon mode")
    parser.add_argument("--api_deamon_file", type=str, default='record.txt', help="api record file")
    parser.add_argument("--api_deamon_file_last", type=str, default='record_last.txt', help="api record last file")
    parser.add_argument("--api_monitor", type=str2bool, default=False, help="api monitor mode")
    parser.add_argument("--api_monitor_file", type=str, default='monitor_file.txt', help="api monitor file")
    args = parser.parse_args()
    if args.api:
        api(args)
    elif args.api_deamon:
        api_deamon(args)
    elif args.api_monitor:
        api_monitor(args)
    else:
        main()

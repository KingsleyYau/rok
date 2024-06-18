import adb

from gui.main_window import MainWindow
import argparse
from api.api import run_api, get_bot
from utils import log

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
    
def api_deamon(args):
    bot = get_bot()
    filepath = 'record.txt'
    while True:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                if len(lines) > 0:
                    line = lines[0]
                    item = json.loads(line)
                    log('item', item)
                    
                    record = item['record']
                    args.run_type = 'request_title'
                    args.title = record['title']
                    args.server = record['server']
                    args.x = record['x']
                    args.y = record['y']
                    
                    run_api(args, bot)
                    # with open(filepath, 'w', encoding='utf-8') as nf:
                    #     nf.writelines(lines)
        except BaseException as e:
            log(e)
        time.sleep(5)
        
def api(args):
    bot = get_bot()
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
        if path == '/api/rok_title':
            if pr:
                args = urllib.parse.parse_qs(pr.query)
                print(pr.path, args)
                query = {k: v[0] for k, v in args.items()}
                query_json = json.dumps(query, ensure_ascii=False)
                
                record = {
                    'server':query['server'],
                    'x':query['x'],
                    'y':query['y'],
                    'title':query['title'],
                }
                print(pr.path, record)
                
                result = False
                try:
                    with open('record.txt', 'r') as f:
                        lines = f.readlines()
                        for line in lines:
                            if line.find(query_json) != -1:
                                item = json.loads(line)
                                rp['errno'] = 1
                                rp['errmsg'] = '请勿重复提交, 上次提交时间' + item['summit_time']
                                result = True
                                break
                except BaseException as e:
                    print(e)
                 
                try:   
                    if not result:
                        summit_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                        item = {
                            'record':record,
                            'summit_time':summit_time
                        }
                        line = json.dumps(item)
                        print('Add', line)
                        with open('record.txt', 'a+') as f:
                            f.write(line + '\n')
                except BaseException as e:
                    print(e)   
        elif path == '/api/rok_title_queue':
            data = {
                'size':0,
                'queue':[],
            }
            with open('record.txt', 'r') as f:
                lines = f.readlines()
                for line in lines:
                    item = json.loads(line)
                    print('Read', item)
                    data['queue'].append(item)
                data['size'] = len(lines)
            rp['data'] = data          
        else:
            rp['errno'] = 1
            
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
    parser.add_argument("--api_deamon", type=str2bool, default=False, help="api mode")
    args = parser.parse_args()
    if args.api:
        api(args)
    # elif args.http:
    #     httpd = HTTPServer(('0.0.0.0', 9527), HttpHandler)
    #     httpd.serve_forever()
    elif args.api_deamon:
        api_deamon(args)
    else:
        main()

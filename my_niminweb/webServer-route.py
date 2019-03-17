import socket
import multiprocessing
import re
import dynamic.mini_frame_route_conDB
import sys


class WebServer(object):

    def __init__(self, my_port=9000):
        # 创建套接字进行挂载  ipv4  数据流 tcp格式传输
        self.tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 设置地址重用
        self.tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        # 绑定端口
        self.tcp_server_socket.bind(('', my_port))
        # 启用侦听状态
        self.tcp_server_socket.listen(128)

    # 处理客户端的http请求
    def handle_client(self, new_client_socket):
        # 接收到客户端请求之后 解码
        request_data = new_client_socket.recv(4096)

        if not request_data:
            print("客户端已经断开")
            new_client_socket.close()
            return

        request = WebServer.decode_fun(request_data)

        request_list = request.split('\r\n')

        # 分解出请求行中的请求路径信息
        result_data = re.search(r'\s(.*)\s', request_list[0])

        # 判断请求路径是否获取到
        if not result_data:
            print("请求的数据格式有错误")
            new_client_socket.close()
            return
        # 拿到路径
        request_path = result_data.group(1)

        if request_path == "/":
            request_path += "index.html"

        # 这里需要分情况处理   1  静态资源   2 动态资源 .py结尾的资源
        # 返回对应的响应信息  （请求行 请求头 请求空行 请求体）
        #  http/1.1 200 ok\r\n
        #  Server: zag-python1.1  Content-Type:text/html  Charset:utf-8\r\n
        #  \r\n
        #  html内容 响应体
        if not request_path.endswith('.html'):
            # 静态资源
            # 尝试打开文件
            # ================
          
            document_root = 'static'
            # ================

            try:
                f = open(document_root + request_path, 'rb')
            except Exception as e:
                # 打开文件错误
                response_line = 'http/1.1 404 NotFound\r\n'
                response_body = '404 Not Found!%s' % e

            else:
                response_line = 'http/1.1 200 ok\r\n'
                response_body = f.read()
                response_body = self.decode_fun(response_body)
            finally:
                response_header = 'Server:zag-python\r\n'
                response_blank = '\r\n'

                send_data = (response_line + response_header + response_blank + response_body).encode()
                # 拼接响应信息 发送给客户端
                new_client_socket.send(send_data)

        else:
            # 动态资源
            # 创建一个字典 用来作为wsgi协议的传递请求参数
            env = dict()
            env['PATH-INFO'] = request_path

            response_header = ''
            response_blank = '\r\n'

            # 动态资源
            response_body = dynamic.mini_frame_route_conDB.application(env, self.set_response_header)
            # 设置响应行
            response_line = 'http/1.1 %s ok\r\n' % self.status
            # 动态拼接响应头信息
            for key, val in self.header_lists:
                response_header += "%s:%s\r\n" % (key, val)

            send_data = (response_line + response_header + response_blank + response_body).encode()
            # 拼接响应信息 发送给客户端
            new_client_socket.send(send_data)

        # 关闭客户端连接
        new_client_socket.close()

    def set_response_header(self, status, header_lists):
        self.status = status
        self.header_lists = header_lists

    @staticmethod
    def decode_fun(data):

        try:
            data = data.decode('utf-8')
        except:
            data = data.decode(encoding="gbk", errors='ignore')

        return data

    def run_forever(self):

        # 开启循环 接收客户端的连接
        while True:
            new_client_socket, ip_port = self.tcp_server_socket.accept()

            print('新客户端已连入：', ip_port)
            # 开启多进程 处理多任务
            p = multiprocessing.Process(target=self.handle_client, args=(new_client_socket,))

            p.start()

            # 主进程中关掉客户端套接字
            new_client_socket.close()


# 在本地作用域下 执行此程序主体
if __name__ == '__main__':
    if len(sys.argv) == 2:
        my_port = int(sys.argv[1])
        ws = WebServer(my_port)
    else:
        # 实例化web服务器类
        ws = WebServer()
        # 执行启动方法

    ws.run_forever()

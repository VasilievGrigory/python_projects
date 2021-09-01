import socket
import pdb
import time
import re
import asyncio


class ClientServerProtocol(asyncio.Protocol):

    
    data_base = {}
    
    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        resp = self.process_data(data.decode())
        self.transport.write(resp.encode('utf8'))

    def get(self, request):
        request = request[4:len(request) - 1]
        print(f"getting...{request}")
        if not re.match('^[a-zA-Z0-9_*+.-]+$', request):
            return "error\nwrong command\n\n"
        ans = "ok\n"
        temp_lst = request.split(' ') if request != "*" else self.data_base.keys()
        for key in temp_lst:
            if key in self.data_base:
                for value in self.data_base[key]:
                    ans += key + ' ' + ' '.join(value) + '\n'
        ans += '\n'
        return ans

    def put(self, request):
        request = request[4:len(request) - 1]
        if not re.match('^[a-zA-Z0-9_*+.-]+ [0-9.]+ [0-9]+$', request):
            return "error\nwrong command\n\n"
        print(f"putting...{request}")
        temp_lst = request.split(' ')
        if not temp_lst[0] in self.data_base:
            self.data_base[temp_lst[0]] = []
        for i in range(0, len(self.data_base[temp_lst[0]])):
            if abs(int(self.data_base[temp_lst[0]][i][1]) - int(temp_lst[2])) < 1:
                self.data_base[temp_lst[0]][i] = (str(float(temp_lst[1])), temp_lst[2])
                print(self.data_base)
                return "ok\n\n"
        self.data_base[temp_lst[0]].append((str(float(temp_lst[1])), temp_lst[2]))
        print(self.data_base)
        return "ok\n\n"

    def process_data(self, message):
        if message.startswith('put'):
            return self.put(message)
        elif message.startswith('get'):
            return self.get(message)
        else:
            return 'error\nwrong command\n\n'


def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(
        ClientServerProtocol,
        host, port
    )

    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == "__main__":
    host = input()
    port = int(input())
    run_server(host, port)

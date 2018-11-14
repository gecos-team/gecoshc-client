#!/usr/bin/env python

import pycos, socket, sys, ssl, os, signal, time
import websocket
import ConfigParser

# Function to get dictionary with the values of one section of the configuration file
def config_section_map(section):
    dict1 = {}
    options = config.options(section)
    for option in options:
        try:
            dict1[option] = config.get(section, option)
        except:
            dict1[option] = None
    return dict1


def ws_send(conn,ws, task=None):
    task.set_daemon()

    thread_pool = pycos.AsyncThreadPool(1)	

    while True:
        try:
            line = yield thread_pool.async_task(ws.recv)
        except Exception as ex:
            print 'Error in server tunnel: %s'%(str(ex))
            break
        if not line:
            break
        yield conn.send(line)
        
    print('End of server tunnel!')
    os.kill(os.getpid(), signal.SIGTERM)

def client_send(conn,ws, task=None):
    task.set_daemon()

    while True:
        try:
            line = yield conn.recv(1024)	
        except Exception as ex:
            print 'Error in client tunnel: %s'%(str(ex))
            break
        if not line:
            break
        ws.send_binary(line)       
        
    print('End of client tunnel!')  
    os.kill(os.getpid(), signal.SIGTERM)

def hcwst(host, port,repeater_ws,proxy_host,proxy_port,proxy_username,proxy_password, ssl_verify, task=None):

    task.set_daemon()
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)	
    sock = pycos.AsyncSocket(sock)
    sock.bind((host, int(port)))
    sock.listen(1)

    print('Tunnel listening at %s' % str(sock.getsockname()))
    if ssl_verify:
        ws = websocket.WebSocket()
    else:
        ws = websocket.WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE})

    if not proxy_host:
        ws.connect(repeater_ws, subprotocols=["binary"],sockopt=(socket.IPPROTO_TCP, socket.TCP_NODELAY))
    else:
        ws.connect(repeater_ws,http_proxy_host=proxy_host,http_proxy_port=proxy_port,http_proxy_auth=proxy_auth, subprotocols=["binary"],sockopt=(socket.IPPROTO_TCP, socket.TCP_NODELAY))	
  
    print('Tunnel connected to %s'% repeater_ws )

    conn, _ = yield sock.accept()
    pycos.Task(client_send, conn,ws)
    pycos.Task(ws_send, conn,ws)


if __name__ == '__main__':

    config = ConfigParser.ConfigParser()
    config.read("/etc/helpchannel.conf")

    server_config = config_section_map("ServerConfig")

    proxy_host = None
    if 'proxy_host' in server_config:
        proxy_host = server_config['proxy_host']
        
    proxy_port = None
    if 'proxy_port' in server_config:
        proxy_port = server_config['proxy_port']
        
    proxy_username = None
    if 'proxy_username' in server_config:
        proxy_username = server_config['proxy_username']
        
    proxy_password = None
    if 'proxy_password' in server_config:
        proxy_password = server_config['proxy_password']

    repeater_ws = config_section_map("TunnelConfig")['tunnel_url']
    local_tunnel_port = config_section_map("TunnelConfig")['local_port']
    ssl_verify = (config_section_map("TunnelConfig")['ssl_verify'] in 
        ['True', 'true', '1', 't', 'y', 'yes'])

    proxy_auth=(proxy_username, proxy_password)

    host, port = '127.0.0.1', int(local_tunnel_port)
    if len(sys.argv) > 1:
        host = sys.argv[1]
    if len(sys.argv) > 2:
        port = int(sys.argv[2])
    pycos.Task(hcwst, host, local_tunnel_port,repeater_ws,proxy_host,proxy_port,proxy_username,proxy_password, ssl_verify)
    if sys.version_info.major > 2:
        read_input = input
    else:
        read_input = raw_input
    while True:
        # Sleep for one minute
        time.sleep(60)

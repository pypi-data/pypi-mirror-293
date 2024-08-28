import grpc
from robomotion import plugin_pb2
from robomotion import plugin_pb2_grpc
from robomotion.error import Error
from robomotion.message import Context, Message
import sys
import time

from asyncio import base_futures
from robomotion.runtime import Runtime
from robomotion.capabilities import get_capabilities


class Node:
    def __init__(self):
        self.guid = ''
        self.name = ''
        self.delayBefore = 0.0
        self.delayAfter = 0.0
        self.continueOnError = False
        self.scope = ''

    def get_var_name(self, var):
        d = {v: k for k, v in globals().items()}
        return d[var]

    def on_create(self):
        pass

    def on_message(self, ctx: Context):
        pass

    def on_close(self):
        pass
    def get_capabilities(self):
        pass


class NodeServicer(plugin_pb2_grpc.NodeServicer):
    def Init(self, request: plugin_pb2.InitRequest, context):
        try:
            channel = grpc.insecure_channel('127.0.0.1:%d' % request.port)
            client = plugin_pb2_grpc.RuntimeHelperStub(channel)
            Runtime.set_client(client=client)
            Runtime.check_runner_conn(channel)

            return plugin_pb2.Empty()

        except Exception as e:
            context.set_code(grpc.StatusCode.UNKNOWN)
            if isinstance(e, Error):
                context.set_details(e.serialize())
            else:
                context.set_details(Error('Err.Unknown', str(e)).serialize())

    def OnCreate(self, request: plugin_pb2.OnCreateRequest, context):
        try:
            Runtime.active_nodes += 1

            config = request.config
            Runtime.factories[request.name].on_create(config)

            return plugin_pb2.OnCreateResponse()

        except Exception as e:
            context.set_code(grpc.StatusCode.UNKNOWN)
            if isinstance(e, Error):
                context.set_details(e.serialize())
            else:
                context.set_details(Error('Err.Unknown', str(e)).serialize())

    def OnMessage(self, request: plugin_pb2.OnMessageRequest, context):
        node = Runtime.nodes[request.guid]
        try:
            data = Runtime.decompress(request.inMessage)

            if request.guid in Runtime.nodes:
                # Sleep with delayBefore on enter
                if node.delayBefore > 0:
                    time.sleep(node.delayBefore)

                ctx = Message(data)
                node.on_message(ctx)
                out_message = ctx.get_raw()

                # Sleep with delayAfter on exit
                if node.delayAfter > 0:
                    time.sleep(node.delayAfter)

                return plugin_pb2.OnMessageResponse(outMessage=out_message)

            return plugin_pb2.OnMessageResponse(outMessage=data)

        except Exception as e:
            if node.continueOnError:
                return plugin_pb2.OnMessageResponse(outMessage=data)

            context.set_code(grpc.StatusCode.UNKNOWN)
            if isinstance(e, Error):
                context.set_details(e.serialize())
            else:
                context.set_details(Error('Err.Unknown', str(e)).serialize())

    def OnClose(self, request: plugin_pb2.OnCloseRequest, context):
        try:
            if request.guid in Runtime.nodes:
                Runtime.nodes[request.guid].on_close()

            Runtime.active_nodes -= 1
            if Runtime.active_nodes <= 0:
                Runtime.event.set()

            return plugin_pb2.OnCloseResponse()

        except Exception as e:
            context.set_code(grpc.StatusCode.UNKNOWN)
            if isinstance(e, Error):
                context.set_details(e.serialize())
            else:
                context.set_details(Error('Err.Unknown', str(e)).serialize())
    def GetCapabilities(self, request: plugin_pb2.Empty, context):        
        return plugin_pb2.PGetCapabilitiesResponse(capabilities=get_capabilities())
          

# -*- encoding: utf-8 -*-

from nameko.cli.run import run

from pyzrpc.meta import CONFIG_MONGO_FIELD_NAME_KEY, CONFIG_MONGO_FIELD_SERVICE_IPADDR_KEY, \
    CONFIG_MONGO_FIELD_SERVICE_VERSION_KEY, CONFIG_MONGO_FIELD_SERVICE_NAME_KEY, \
    CONFIG_MONGO_FIELD_SERVICE_PID_KEY, CONFIG_MONGO_FIELD_SERVICE_FUNCTIONS_KEY

from pyzrpc.observer import Observer
from pyzrpc.logger import Logger
from pyzrpc.utils import RpcProxy
from pyzrpc.mongo import DBServices

from pyzrpc.service.service_constructor import ServiceBuild


class _ServiceStart:

    @staticmethod
    def service_start(service, config):
        _observer = Observer()

        _logger = Logger()
        _rpc_proxy = RpcProxy()
        _mongo = DBServices()

        _observer.config = config
        _observer.attach(_logger)
        _observer.attach(_rpc_proxy)
        _observer.attach(_mongo)
        _observer.notify()

        build = ServiceBuild()
        _cls = build.build(cls_path=service.__file__, rpc_proxy=_rpc_proxy, logger=_logger)

        _logger.logger(_cls.service_name).info('service running : {}'.format(_cls.name))

        import os
        _mongo.update_many(
            query={
                CONFIG_MONGO_FIELD_NAME_KEY: _cls.name,
                CONFIG_MONGO_FIELD_SERVICE_IPADDR_KEY: _cls.service_ipaddr
            },
            update_data={
                CONFIG_MONGO_FIELD_NAME_KEY: _cls.name,
                CONFIG_MONGO_FIELD_SERVICE_IPADDR_KEY: _cls.service_ipaddr,
                CONFIG_MONGO_FIELD_SERVICE_NAME_KEY: _cls.service_name,
                CONFIG_MONGO_FIELD_SERVICE_VERSION_KEY: _cls.service_version,
                CONFIG_MONGO_FIELD_SERVICE_PID_KEY: os.getpid(),
                CONFIG_MONGO_FIELD_SERVICE_FUNCTIONS_KEY: _cls.functions
            },
            upsert=True
        )

        import eventlet
        eventlet.monkey_patch()
        run(services=[_cls], config=_rpc_proxy.rpc_config)

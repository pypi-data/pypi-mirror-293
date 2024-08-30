import argparse
import logging
import pickle
import socketserver
import struct


class LogRecordStreamRequestHandler(socketserver.StreamRequestHandler):
    def handle(self):
        while True:
            # The meaning of the first 4 bytes:
            # https://docs.python.org/zh-cn/3/library/logging.handlers.html#logging.handlers.SocketHandler.makePickle
            chunk = self.request.recv(4)
            # Invalid record, skip this log
            if len(chunk) < 4:
                break
            data_len = struct.unpack('>L', chunk)[0]
            chunk = self.request.recv(data_len)
            while len(chunk) < data_len:
                chunk = chunk + self.request.recv(data_len - len(chunk))
            obj = self.unpickle(chunk)
            record = logging.makeLogRecord(obj)
            self.handle_log_record(record)

    @staticmethod
    def unpickle(data):
        return pickle.loads(data)

    def handle_log_record(self, record: logging.LogRecord):
        logger = logging.getLogger(record.name)
        # N.B. EVERY record gets logged. This is because Logger.handle
        # is normally called AFTER logger-level filtering. If you want
        # to do filtering, do it at the client end to save wasting
        # cycles and network bandwidth!
        logger.handle(record)


def main():
    parser = argparse.ArgumentParser(description='Log server')
    parser.add_argument('port', type=int)
    parser.add_argument('-H', '--hostname', type=str, default='localhost')
    parser.add_argument(
        '-f',
        '--format',
        type=str,
        default='[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s',
        help='Log format',
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG,
        format=args.format,
    )

    server = socketserver.TCPServer(
        (args.hostname, args.port), LogRecordStreamRequestHandler
    )
    print(f'Listening on {args.hostname}:{args.port}')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()

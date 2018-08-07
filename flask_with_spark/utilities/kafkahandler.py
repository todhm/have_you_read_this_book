from kafka import KafkaProducer
import logging
import json


class KafkaLoggingHandler(logging.Handler):

    def __init__(self, hosts_list, topic, **kwargs):
        logging.Handler.__init__(self)
        self.key = kwargs.get("key", None)
        self.topic = topic
        self.producer = KafkaProducer(
            bootstrap_servers=hosts_list,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            linger_ms=10
            )

    def flush(self, timeout=None):
        """Flush the objects."""
        self.producer.flush(timeout=timeout)

    def emit(self, record):
        """Emit the provided record to the kafka_client producer."""
        # drop kafka logging to avoid infinite recursion
        print(record,record.name,'--------------')
        if 'kafka.' in record.name:
            return

        try:
            # apply the logger formatter
            msg = self.format(record)
            self.producer.send(self.topic, {'message': msg})
            self.flush(timeout=1.0)
        except Exception:
            logging.Handler.handleError(self, record)

    def close(self):
        """Close the producer and clean up."""
        self.acquire()
        try:
            if self.producer:
                self.producer.close()
            logging.Handler.close(self)
        finally:
            self.release()

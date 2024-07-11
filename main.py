import functions_framework

import logging
import os
import random
import sys
import string
import time

from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
from opentelemetry.sdk._logs.export import ConsoleLogExporter
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.resources import Resource

from dynatrace.opentelemetry.gcf import wrap_handler
from dynatrace.opentelemetry.tracing.api import configure_dynatrace

logger_provider = LoggerProvider(
    resource=Resource.create(
        {
            "service.name": "train-the-telemetry"
        }
    ),
)
set_logger_provider(logger_provider)

otlp_exporter = OTLPLogExporter()
logger_provider.add_log_record_processor(BatchLogRecordProcessor(otlp_exporter))

# console_exporter = ConsoleLogExporter()
# logger_provider.add_log_record_processor(BatchLogRecordProcessor(console_exporter))

# handler = LoggingHandler()
handler = LoggingHandler(level=logging.NOTSET, logger_provider=logger_provider)

# Practice The Telemetry
def practice(how_long):
    practice_logger = logging.getLogger("yoda.practice")
    practice_logger.setLevel(logging.INFO)
    start_time = time.time()
    try:
        how_long_int = int(how_long)
        practice_logger.info("Starting to practice The Telemetry for %i second(s)", how_long_int)
        while time.time() - start_time < how_long_int:
            next_char = random.choice(string.punctuation)
            print(next_char, end="", flush=True)
            time.sleep(0.5)
        practice_logger.info("Done practicing")
    except ValueError as ve:
        practice_logger.error("I need an integer value for the time to practice: %s", ve)
        return False
    except Exception as e:
        practice_logger.error("An unexpected error occurred: %s", e)
        return False
    return True

# Main function
@wrap_handler
@functions_framework.http
def hello_http(request):
    # Attach OTLP handler to root logger
    logging.getLogger().addHandler(handler)
    main_logger = logging.getLogger("yoda.main")
    main_logger.setLevel(logging.INFO)
    
    result = practice(1)
    main_logger.info("Practicing The Telemetry completed: %s", result)
    logger_provider.shutdown()
    return 'Practicing The Telemetry completed!'
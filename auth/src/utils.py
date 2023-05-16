import opentelemetry.trace
from flask import request
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from src.core import base_config, jaeger_config, logger


def before_request_log():
    logger.info(f"{request.method}: {request.path}")
    logger.debug(f"{request.args}")
    if (
        request.content_type == "application/json"
        and int(request.headers.get("Content-Length")) > 0
    ):
        logger.debug(f"{request.get_json()}")


def after_request_log(response):
    logger.debug(
        f"Response for {request.method} {request.path}: {response.get_json()}",
    )
    return response


def before_request_jaeger():
    request_id = request.headers.get("X-Request-Id")
    if not request_id:
        raise RuntimeError("request id is required")


def configure_tracer() -> None:
    opentelemetry.trace.set_tracer_provider(
        TracerProvider(
            resource=Resource.create(attributes={SERVICE_NAME: base_config.COMMON_SERVICE_NAME})
        )
    )
    opentelemetry.trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(
            JaegerExporter(
                agent_host_name=jaeger_config.JAEGER_HOSTNAME,
                agent_port=jaeger_config.JAEGER_SERVICE_PORT,
            )
        )
    )
    opentelemetry.trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(ConsoleSpanExporter())
    )

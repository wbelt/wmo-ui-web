import os
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import SERVICE_NAME, SERVICE_NAMESPACE, SERVICE_INSTANCE_ID, Resource
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter

bind = "0.0.0.0:8000"

workers = 2
worker_class = "uvicorn.workers.UvicornWorker"

# Sample logging
# errorlog = "-"
# loglevel = "info"
# accesslog = "-"
# access_log_format = (
#     '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
# )

def post_fork(server, worker):
    server.log.info("Worker spawned (pid: %s)", worker.pid)
    
    trace.set_tracer_provider(
        TracerProvider(
            resource=Resource.create(
                {
                    SERVICE_NAME: "dashboard",
                    SERVICE_NAMESPACE: "wmo.ui.web",
                    SERVICE_INSTANCE_ID: f"{os.environ.get('WEBSITE_HOSTNAME','unknown')}.pid-{worker.pid}",
                }
            )
        )
    )
    traceExporter = AzureMonitorTraceExporter.from_connection_string(os.environ['CS_APPINSIGHTS'])
    span_processor = BatchSpanProcessor(traceExporter)
    trace.get_tracer_provider().add_span_processor(span_processor)


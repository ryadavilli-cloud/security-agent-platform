from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter
from services.shared.config import settings

def setup_tracing(service_name: str = "ai-security-auditor"):
    if not settings.appinsights_conn:
        return
    resource = Resource.create({"service.name": service_name})
    tp = TracerProvider(resource=resource)
    exporter = AzureMonitorTraceExporter.from_connection_string(settings.appinsights_conn)
    tp.add_span_processor(BatchSpanProcessor(exporter))
    trace.set_tracer_provider(tp)

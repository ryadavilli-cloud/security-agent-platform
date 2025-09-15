from azure.cosmos import CosmosClient, PartitionKey, exceptions
from services.shared.config import settings

DB_NAME = settings.cosmos_db
CONTAINERS = [
    ("users", "/userId"),
    ("sessions", "/sessionId"),
    ("conversations", "/sessionId"),
    ("audit_logs", "/sessionId"),
    ("security_findings", "/repoId"),
    ("agents", "/agentType"),
    ("knowledge_base", "/category"),
]

_client = CosmosClient(settings.cosmos_endpoint, credential=settings.cosmos_key)
_db = _client.create_database_if_not_exists(id=DB_NAME)

def ensure_containers():
    for name, pk in CONTAINERS:
        try:
            _db.create_container_if_not_exists(id=name, partition_key=PartitionKey(path=pk))
        except exceptions.CosmosResourceExistsError:
            pass

def container(name: str):
    return _db.get_container_client(name)

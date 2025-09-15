import time, uuid
from services.shared.cosmos import ensure_containers, container

def run():
    ensure_containers()
    agents = container("agents")
    kb = container("knowledge_base")
    seed_agents = [
        {"id": "agent_code_analyzer", "agentType": "code", "tools": ["static_scan","pattern_match"]},
        {"id": "agent_threat_intel", "agentType": "threat", "tools": ["cve_lookup"]},
        {"id": "agent_compliance", "agentType": "compliance", "tools": ["rag_lookup"]},
        {"id": "agent_reporter", "agentType": "report", "tools": ["summarize"]},
    ]
    for a in seed_agents:
        try: agents.create_item(a)
        except Exception: pass
    for cat in ["owasp","cwe","soc2","nist"]:
        try: kb.create_item({"id": f"kb_{cat}", "category": cat, "ts": time.time(), "docs": []})
        except Exception: pass

if __name__ == "__main__":
    run()
    print("Seed complete.")

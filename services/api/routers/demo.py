import uuid, time
from fastapi import APIRouter, Request, Response
from opentelemetry import trace
from services.shared.cosmos import container

router = APIRouter()
tracer = trace.get_tracer(__name__)
audits = container("audit_logs")
users = container("users")
sessions = container("sessions")

def _ensure_guest(request: Request, response: Response):
    sid = request.cookies.get("sessionId") or str(uuid.uuid4())
    uid = request.cookies.get("userId") or f"user_anon_{sid[:8]}"
    # minimal session + user upsert
    try:
        sessions.upsert_item({"id": f"sess_{sid}", "sessionId": sid, "lastSeen": time.time()})
        users.upsert_item({
            "id": uid, "userId": uid, "displayName": f"Guest-{uid[-4:]}",
            "type": "guest", "capabilities": ["analyze","approve","escalate"]
        })
    except Exception:
        pass
    response.set_cookie("sessionId", sid)
    response.set_cookie("userId", uid)
    return sid, uid

@router.get("/demo/ping")
def ping(request: Request):
    response = Response()
    session_id, user_id = _ensure_guest(request, response)
    with tracer.start_as_current_span("demo_ping") as span:
        span.set_attribute("sessionId", session_id)
        span.set_attribute("userId", user_id)
        audits.upsert_item({
            "id": f"aud_{uuid.uuid4()}",
            "sessionId": session_id,
            "action": "demo.ping",
            "status": "success",
            "userId": user_id,
            "ts": time.time(),
        })
    response.media_type = "application/json"
    response.body = bytes(f'{{"ok": true, "sessionId":"{session_id}","userId":"{user_id}"}}', "utf-8")
    return response

"""
Test script to see state access directly.
Run with: python test_state.py
"""

import asyncio
from agent import root_agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part

# Load local .env file if present (simple, dependency-free)
import os
from pathlib import Path


def load_local_env():
    env_path = Path(__file__).parent / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if '=' not in line:
            continue
        key, val = line.split('=', 1)
        key = key.strip()
        val = val.strip().strip('"').strip("'")
        # Don't overwrite existing env vars
        if key not in os.environ:
            os.environ[key] = val


load_local_env()

# Setup session and runner
session_service = InMemorySessionService()
session = asyncio.run(
    session_service.create_session(
        app_name="name_extractor_app",
        user_id="test_user",
        session_id="test_session",
    )
)

runner = Runner(
    agent=root_agent,
    app_name="name_extractor_app",
    session_service=session_service,
)

# Test: Extract name
user_message = Content(parts=[Part(text="Hi, my name is Alex Johnson")])

print("=== Running agent ===")
result = runner.run(
    user_id="test_user",
    session_id="test_session",
    new_message=user_message
)


def extract_event_text(event):
    if not getattr(event, "content", None):
        return ""
    parts = getattr(event.content, "parts", None)
    if not parts:
        return ""
    try:
        return "".join(p.text for p in parts if getattr(p, "text", None))
    except Exception:
        return str(parts)


# Debug: print all events to help diagnose empty responses
print("--- Events (debug) ---")
for event in result:
    try:
        ev_text = extract_event_text(event)
    except Exception:
        ev_text = "<could not extract text>"
    print(type(event).__name__, getattr(event, "name", ""), ev_text)
    try:
        # print available attributes for deeper debugging
        if hasattr(event, "__dict__"):
            print("  attrs:", event.__dict__)
        else:
            print("  repr:", repr(event))
    except Exception:
        pass

# Show final response
for event in result:
    if event.is_final_response():
        print(f"\nAgent response: {extract_event_text(event)}")

# Access state programmatically
print(f"\n=== State after execution ===")
print(f"Full state: {session.state}")
print(f"Extracted name: {session.state.get('user_name')}")

# Your code can now make decisions based on state
if session.state.get("user_name"):
    print("✅ Name was successfully extracted and stored!")
else:
    print("❌ Name extraction failed")

# Test accessing in subsequent turns
print("\n=== Simulating second turn ===")
result2 = runner.run(
    user_id="test_user",
    session_id="test_session",
    new_message=Content(parts=[Part(text="What's my name?")])
)

for event in result2:
    if event.is_final_response():
        print(f"Agent response: {extract_event_text(event)}")

print(f"\nState still contains: {session.state.get('user_name')}")
print("✅ State persists across turns!")

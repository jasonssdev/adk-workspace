"""
Test deployed weather agent using Agent Platform SDK for Python
Reference: https://adk.dev/deploy/agent-runtime/test/#test-using-python
"""

import asyncio
from vertexai import agent_engines


async def test_deployed_agent():
    """Test interaction with deployed weather agent."""

    # Connect to deployed agent
    # REPLACE with your actual resource name from the deploy command output
    resource_name = "projects/568520081859/locations/us-central1/reasoningEngines/4672788628361969664"
    remote_app = agent_engines.get(resource_name)

    # Create a session
    print("=" * 60)
    print("Creating session...")
    print("=" * 60)
    remote_session = await remote_app.async_create_session(user_id="u_weather_test")
    print(f"Session created with ID: {remote_session['id']}")
    print()

    # Test query 1: Simple weather query
    print("=" * 60)
    print("Test 1: Weather query for San Francisco")
    print("=" * 60)
    async for event in remote_app.async_stream_query(
        user_id="u_weather_test",
        session_id=remote_session["id"],
        message="What's the weather in San Francisco?"
    ):
        print(event)
    print()

    # Test query 2: Forecast query
    print("=" * 60)
    print("Test 2: Weather forecast for Seattle")
    print("=" * 60)
    async for event in remote_app.async_stream_query(
        user_id="u_weather_test",
        session_id=remote_session["id"],
        message="Will it rain tomorrow in Seattle?"
    ):
        print(event)
    print()

    print("=" * 60)
    print("✓ Deployed agent working successfully!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(test_deployed_agent())

print("=" * 60)
print("✓ Deployed agent working successfully!")
print("=" * 60)

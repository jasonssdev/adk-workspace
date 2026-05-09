from google.adk.agents import LlmAgent

root_agent = LlmAgent(
    model='gemini-2.5-flash',
    name='weather_agent',
    description='Weather agent on Cloud Run',
    instruction="""
        You are a helpful weather assistant.
        Provide weather information for cities worldwide.
    """
)

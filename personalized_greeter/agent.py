"""
Personalized Greeter - Demonstrates State Templating
Shows how {var} templating injects state values into instructions.

Reference: https://google.github.io/adk-docs/sessions/state.md
"""

from google.adk.agents import LlmAgent

# Agent with state templating
root_agent = LlmAgent(
    model='gemini-2.5-flash',
    name='personalized_greeter',
    instruction="""
You are a friendly assistant.

User information:
 - Name: {user_name?there}
 - Preferred language: {user_language?English}
 - Membership: {membership_tier?free}

{membership_tier?Your membership level is: {membership_tier}}

Greet the user warmly and offer assistance.
Respond in {user_language?English}.
"""
)

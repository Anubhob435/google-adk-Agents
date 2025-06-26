from google.adk.agents import LlmAgent, BaseAgent


# Define individual agents
greeter = LlmAgent(
    name="greeter",
    model="gemini-2.0-flash",
    instruction="You are a friendly greeter agent. Your role is to welcome users, introduce yourself, and provide warm, friendly interactions. Always be polite, enthusiastic, and helpful in your greetings.",
    description="A friendly agent that handles user greetings and introductions."
)

task_executor = LlmAgent(
    name="task_executor", 
    model="gemini-2.0-flash",
    instruction="You are a task execution agent. Your role is to understand user requests, break them down into actionable steps, and execute tasks efficiently. Focus on being practical, organized, and thorough in completing assigned tasks.",
    description="An agent specialized in understanding and executing various tasks and requests."
)

# Create parent agent and assign children via sub_agents
coordinator = LlmAgent(
    name="Coordinator",
    model="gemini-2.0-flash",
    instruction="You are a coordinator agent that manages interactions between the greeter and task executor agents. Route user requests to the appropriate sub-agent based on the nature of their request. If it's a greeting or introduction, use the greeter. If it's a task or request for action, use the task executor.",
    description="I coordinate greetings and tasks between specialized sub-agents.",
    sub_agents=[ # Assign sub_agents here
        greeter,
        task_executor
    ]
)
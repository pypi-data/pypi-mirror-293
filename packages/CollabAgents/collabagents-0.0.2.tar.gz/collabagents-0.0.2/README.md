# CollabAgents

**CollabAgents** is a versatile Python framework that allows developers to create intelligent AI agents with various roles and tools. The framework supports the creation of Assistant agents (e.g., CEO, Manager, Developer) that can work together within or across companies to complete complex user requests. The unique capability of CollabAgents lies in its ability to simulate real-world business processes, where multiple AI-driven companies interact to achieve specific goals.

## Features

- **Create AI Agents with Tools**: Easily build AI agents equipped with a wide range of tools, from Python execution to file operations and terminal commands.
- **Assistant Agents**: Define assistant agents like CEOs, Managers, and Developers, each with specific roles and responsibilities.
- **Interacting Companies**: Simulate business scenarios where multiple companies collaborate to fulfill user requirements.
- **Flexible Integration**: Supports both Anthropic and OpenAI models, allowing you to choose the best fit for your needs.

## Example Use Case

Here’s an example of how to create a Python Developer agent using CollabAgents:

```python
import asyncio
from CollabAgents.agent import StructuredAgent
from CollabAgents.models import AnthropicModel
from CollabAgents.tools.PythonTool import RunPythonFile
from CollabAgents.tools.FileOperationsTool import CreateFolder, SaveFile, ListFilesInDirectory
from CollabAgents.helper import print_colored

description = "Responsible for Answering User questions."
instruction = "You are a helpful Assistant."
tools = [CreateFolder, SaveFile, ListFilesInDirectory, RunPythonFile]

api_key = 'YOUR_API_KEY'

model = AnthropicModel(model_name='claude-3-haiku-20240307', api_key=api_key)

agent = StructuredAgent(model, "AI Assistant", description, instruction, tools, max_allowed_attempts=50)

if __name__ == "__main__":
    async def main():
        print_colored("Starting the application...........", "green")
        user_input = input("User Input: ")
        messages = []
        while user_input != "bye":
            output = await agent.run(user_input, messages)
            messages = agent.messages
            user_input = input("User Input: ")

    asyncio.run(main())
```
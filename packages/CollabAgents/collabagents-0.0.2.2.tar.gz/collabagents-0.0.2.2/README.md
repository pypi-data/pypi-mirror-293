# CollabAgents

<div align="center">
    <img src="logo.webp" alt="CollabAgents Logo" width="400"/> <!-- Adjust width as needed -->
</div>


**CollabAgents** is a versatile Python framework designed for creating intelligent AI agents that can perform a wide range of tasks. It supports the development of agents equipped with various tools, allowing them to collaborate within and across companies to fulfill complex user requests. The framework’s unique strength lies in its ability to simulate real-world business processes, where multiple AI-driven entities interact to achieve specific goals.

## Features

- **Create AI Agents with Tools**: Easily build AI agents with a diverse set of tools, from Python execution to file operations and terminal commands.
- **Role-Based Agents**: Define agents with specific roles and responsibilities to handle different tasks and collaborate effectively.
- **Interacting Entities**: Simulate scenarios where multiple agents or companies work together to complete user requests.
- **Flexible Integration**: Supports both Anthropic and OpenAI models, providing flexibility in choosing the best AI model for your needs.

## Installation

You can install the CollabAgents framework using pip:

```bash

pip install CollabAgents

```

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

## License
This project is licensed under the MIT License. - see the LICENSE file for details.

## For More Tutorials Visit My Youtube Channel:

- [Watch Tutorials on YouTube](https://www.youtube.com/@learnwithvichu) <!-- Replace with your actual YouTube channel link -->
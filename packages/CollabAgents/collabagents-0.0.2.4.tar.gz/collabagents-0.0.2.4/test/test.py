# Python Developer
import asyncio
from CollabAgents.helper import print_colored
from CollabAgents.agent import StructuredAgent
from CollabAgents.tools.PythonTool import RunPythonFile
from CollabAgents.models import AnthropicModel,OpenaiChatModel
from CollabAgents.tools.TerminalTool import ExecuteTerminalCommand
from CollabAgents.tools.FileOperationsTool import SaveFile,CreateFolder,ListFilesInDirectory,AppendToFile
# from CollabAgents.tools.AgenticTools import DescribePlots

import sys
sys.dont_write_bytecode =True

description = "Responsible for Answering User question."

instruction = "You are an helpful assistant."

tools = [CreateFolder,SaveFile,AppendToFile,ListFilesInDirectory,RunPythonFile]

openai_api_key = ''

model = OpenaiChatModel(model_name="gpt-4o-mini",api_key=openai_api_key,verbose=True)

# api_key='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'

# model = AnthropicModel(model_name= 'claude-3-haiku-20240307',api_key=api_key)

agent = StructuredAgent(model,"AI Assistant",description,instruction,tools,max_allowed_attempts=50)

if __name__=="__main__":

    async def main():

        print_colored("Starting the application...........","green")

        user_input = input("User Input : ")

        messages = []

        while user_input!="bye":

            # print_colored(f"User : {user_input}","teal")

            output = agent.run(user_input,messages)

            messages = agent.messages

            # print_colored(f"Assistant : {output}","purple")

            user_input = input("User Input : ")

    asyncio.run(main())
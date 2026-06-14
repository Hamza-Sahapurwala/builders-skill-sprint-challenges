"""
Challenge 5 (Innovate): Build Your Own MCP-Powered Agent

YOUR TASK:
  Build an innovative agent from scratch that connects to any MCP server.
  The most creative and useful agent gets a special shoutout! 🏆

RULES:
  - Must use Strands Agents SDK
  - Must use at least one MCP server
  - Must use Amazon Nova Pro (or any Bedrock model)
  - Must have an interactive chat loop
  - Must be YOUR OWN idea — be creative!

EXAMPLE MCP SERVERS:
  pip install awslabs.aws-documentation-mcp-server   # AWS Docs
  uvx awslabs.cdk-mcp-server@latest                  # AWS CDK
  uvx awslabs.cost-analysis-mcp-server@latest        # AWS Pricing

BROWSE MORE: https://github.com/modelcontextprotocol/servers

RESOURCES:
  - Strands MCP docs: https://strandsagents.com/latest/user-guide/concepts/tools/mcp-tools/
  - AWS MCP servers: https://github.com/awslabs/mcp

Build something that makes us go "whoa!" 🚀
"""

# Your code here — build the entire agent from scratch!

import os
import sys
import asyncio
import boto3
from mcp import stdio_client, StdioServerParameters
from strands import Agent
from strands.models.bedrock import BedrockModel
from strands.tools.mcp import MCPClient

# 1. Initialize AWS Session & Amazon Nova Pro via Bedrock
# Note: Nova Pro is optimized via cross-region inference profiles (e.g., us.amazon.nova-pro-v1:0)
session = boto3.Session(
    region_name=os.environ.get("AWS_DEFAULT_REGION")
)

print("Initializing Amazon Nova Pro via Bedrock...")
nova_model = BedrockModel(
    model_id="us.amazon.nova-pro-v1:0",
    boto_session=session,
    temperature=0.2,
    max_tokens=4096
)

# 2. Setup the AWS Documentation Model Context Protocol (MCP) Server Client
# This dynamically spins up the server via uvx tool extraction
print("Connecting to AWS Documentation MCP Server...")
aws_docs_mcp = MCPClient(
    lambda: stdio_client(
        StdioServerParameters(
            command="uvx",
            args=["awslabs.aws-documentation-mcp-server@latest"]
        )
    )
)

# 3. Define the Agent Architecture & System Directive
SYSTEM_PROMPT = """You are an expert DevOps and AWS Infrastructure Assistant. 
Your core responsibility is helping developers build clean, secure, and modern AWS CDK code blocks.
Whenever you are asked about specific infrastructure design, patterns, or errors:
1. Use your AWS Documentation tool to look up current guidance, resource names, and best practices.
2. Provide executable AWS CDK (Python/TypeScript) code snippets.
3. Be succinct, professional, and emphasize AWS Well-Architected framework standards.
"""

devops_agent = Agent(
    model=nova_model,
    tools=[aws_docs_mcp],
    system_prompt=SYSTEM_PROMPT
)

# 4. Interactive Chat Loop
def interactive_chat():
    print("\n==========================================================")
    print("🚀 CloudOps Assistant Powered by Strands SDK & Nova Pro")
    print("==========================================================")
    print("Ask infrastructure questions or ask for CDK snippets. Type 'exit' to quit.\n")
    
    while True:
        try:
            user_input = input("✨ DevOps Tool > ")
            if user_input.strip().lower() in ['exit', 'quit']:
                print("Disconnecting tools and shutting down. Standby...")
                break
                
            if not user_input.strip():
                continue
                
            # Invoke the agent loop (It will automatically handle planning, 
            # tool invocation from MCP, and reasoning steps under the hood)
            response = devops_agent(user_input)
            
            print("\n🤖 Assistant Response:")
            print("-" * 40)
            print(response)
            print("-" * 40 + "\n")
            
        except KeyboardInterrupt:
            print("\nGracefully exiting...")
            break
        except Exception as e:
            print(f"\n❌ Error encountered: {e}\n")

if __name__ == "__main__":
    interactive_chat()
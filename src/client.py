import asyncio, json, sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from pathlib import Path

async def testExternalAPITool(session):
    # Initialize the connection
    await session.initialize()

    # List available tools
    tools_result = await session.list_tools()
    print("Available tools:")
    for tool in tools_result.tools:
        print(f"  - {tool.name}: {tool.description}")

    allTools = ["getTypesOfSources", "getNamesOfSources", "getNumberOfSources"]
    chosenTool = allTools[0] 

    toolResult = await session.call_tool(chosenTool, arguments={ 
        "country":"japan",
    })
    
    result = json.loads(toolResult.model_dump_json())

    print(f"The results are: {result['content'][0]['text']}")


async def testDockerHubTool(session):
    await session.initialize()
    
    # Pull the docker image
    print("Pulling docker image: python:3.8-slim")
    pull_result = await session.call_tool("run_docker_command", arguments={"command": "pull python:3.8-slim"})
    pull_content = json.loads(pull_result.content[0].text)
    if "error" in pull_content:
        print(f"Error pulling image: {pull_content['error']}\n{pull_content.get('stderr', '')}")
        return
    print("Pull complete.")
    print(pull_content.get('stdout'))


    # Run the docker image to get python version
    print("\nRunning docker image to get python version...")
    run_result = await session.call_tool("run_docker_command", arguments={"command": "run --rm python:3.09-slim python --version"})
    run_content = json.loads(run_result.content[0].text)
    if "error" in run_content:
        print(f"Error running image: {run_content['error']}\n{run_content.get('stderr', '')}")
        return
    
    print("Python version:")
    print(run_content.get('stdout'))

async def clientMain(input):

    current_dir = Path.cwd()
    if current_dir.name == "src":
        serverPath = "mcpserver.py"
    else:
        serverPath = "./src/mcpserver.py"
        
    # Define server parameters
    server_params = StdioServerParameters(
        command="python",
        args=[serverPath, "stdio"],
    )

    # Connect to the server
    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            if (input == 'api'):
                await testExternalAPITool(session)
            elif (input == 'docker'):
                await testDockerHubTool(session)

if __name__ == "__main__":
    validTest = ['api', 'docker']
    if (len(sys.argv) > 1 and sys.argv[1] in validTest):
        test = sys.argv[1]
    else:
        test = 'api'
    asyncio.run(clientMain(test))
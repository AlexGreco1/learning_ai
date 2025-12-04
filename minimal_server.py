
import asyncio
from mcp import Server
import mcp.server.stdio

class SimpleServer(Server):
    def __init__(self):
        super().__init__("simple-tool")

    async def list_tools(self):
        return [{
            "name": "greet",
            "description": "Greet someone by name",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Name to greet"}
                },
                "required": ["name"]
            }
        }]

    async def call_tool(self, name: str, arguments: dict):
        if name == "greet":
            return [{"type": "text", "text": f"Hello, {arguments['name']}!"}]

async def main():
    server = SimpleServer()
    async with mcp.server.stdio.stdio_server() as (read, write):
        await server.run(read, write, mcp.NotificationOptions())

asyncio.run(main())

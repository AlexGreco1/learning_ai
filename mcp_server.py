
import asyncio
import sys
import json
from mcp import Server, NotificationOptions
import mcp.server.stdio

# Create MCP server instance
server = Server("simple-tool")

@server.list_tools()
async def handle_list_tools():
    """List available tools - required MCP method"""
    return [
        {
            "name": "add",
            "description": "Add two numbers",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"}
                },
                "required": ["a", "b"]
            }
        },
        {
            "name": "multiply",
            "description": "Multiply two numbers",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"}
                },
                "required": ["a", "b"]
            }
        },
        {
            "name": "greet",
            "description": "Greet someone",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Name to greet"}
                },
                "required": ["name"]
            }
        }
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]):
    """Handle tool calls - required MCP method"""
    if name == "add":
        result = arguments["a"] + arguments["b"]
        return [{
            "type": "text",
            "text": f"Result: {result}"
        }]
    elif name == "multiply":
        result = arguments["a"] * arguments["b"]
        return [{
            "type": "text",
            "text": f"Result: {result}"
        }]
    elif name == "greet":
        return [{
            "type": "text",
            "text": f"Hello, {arguments['name']}!"
        }]
    else:
        raise ValueError(f"Unknown tool: {name}")

async def main():
    """Main server function - runs the MCP server over stdio"""
    print("MCP Server starting...", file=sys.stderr)
    sys.stderr.flush()

    # Create stdio server connection
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        # Run the server with the specified streams
        await server.run(
            read_stream,
            write_stream,
            NotificationOptions()
        )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server shutting down...", file=sys.stderr)
    except Exception as e:
        print(f"Server error: {e}", file=sys.stderr)

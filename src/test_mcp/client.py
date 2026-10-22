import anyio

from mcp import Client, StdioServerParameters


server_parameters = StdioServerParameters(
    command="uv",
    args=["run", "python", "src/test_mcp/server.py"],
)


async def main():
    async with Client(server_parameters) as client:

        print("Connected to MCP server.")

        tools_result = await client.list_tools()

        print("\nAvailable tools:")

        for tool in tools_result.tools:
            print(f"- {tool.name}: {tool.description}")

        while True:
            print("\nOptions:")
            print("1. Search documents")
            print("2. Read a file")
            print("3. Perform an action")
            print("4. Exit")

            choice = input("\nChoose an option: ").strip()

            if choice == "1":
                query = input("Search query: ")

                result = await client.call_tool(
                    "search_documents",
                    {"query": query},
                )

            elif choice == "2":
                filename = input("Filename: ")

                result = await client.call_tool(
                    "read_file",
                    {"filename": filename},
                )

            elif choice == "3":
                action = input(
                    "Action (create_note/delete_note): "
                ).strip()

                target = input("Target filename: ").strip()

                content = ""

                if action == "create_note":
                    content = input("Note content: ")

                result = await client.call_tool(
                    "perform_action",
                    {
                        "action": action,
                        "target": target,
                        "content": content,
                    },
                )

            elif choice == "4":
                print("Disconnecting.")
                break

            else:
                print("Invalid option.")
                continue

            print("\nServer response:")
            for item in result.content:
                if item.type == "text":
                    print(item.text)

            if result.is_error:
                print("The tool reported an error.")


if __name__ == "__main__":
    anyio.run(main)
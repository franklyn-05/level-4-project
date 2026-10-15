# Exploring Existing MCP 

In looking to construct my own MCP server to 'attack' using some of the exploits I previously researched, I researched some available software for MCP server implementation. Here are some of the notable tools I found.

---

## 1. [AppSec's Vulnerable MCP Lab](https://github.com/appsecco/vulnerable-mcp-servers-lab/tree/main)
  - This repo contains a number of deliberately vulnerable MCP servers, designed to test some common attacks such as prompt injection, malicious user action, namespace typosquatting etc. It demonstrates how to run these servers and demonstrates the attacks.

---

## 2. [Official Model Context Protocol Servers](https://github.com/modelcontextprotocol/servers)
  - This contains a collection of MCP servers for a number of languages such as Python, Java, C# and more. It also has numerous reference servers for tools like Git, Filesystem and Memory. Finally, the repo contains a list of archived servers for services such as Github, Google Drive, PostgreSQL and more. It provides a good reference for good implementation practice for developing an MCP server.

--- 


## 3. [Official Python MCP SDK](https://py.sdk.modelcontextprotocol.io/#create-it)
  - This is the official documentation for Python's MCP development toolkit. It provides documentation on how to implement your own MCP server with its own tools and resources as well as implementing MCP client to interact with the server.
    - It has built in plugins for server and client side.
    - This will be the best method for implementing the ecosystem - as I can run it natively on my Mac and easily link to LLM's through their API's.
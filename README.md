# Snowflake Agent for MCP Server

This is a custom AI agent that connects to Snowflake using SQLAlchemy and integrates with an **MCP (Model Context Protocol) Server** to allow seamless SQL query execution on Snowflake databases. The agent is designed to be used within agentic AI ecosystems where tools are registered via MCP servers.

## 🧩 Features

- Connects to **Snowflake** using external browser authentication.
- Supports executing **SQL queries** on specified databases and schemas.
- Works as a tool registered to an **MCP server**.
- Built-in connection pooling using **SQLAlchemy QueuePool**.
- Returns query results as structured JSON.

## 🚀 Architecture

This agent is built on top of:
- **FastMCP** from `mcp.server.fastmcp` for tool registration and serving.
- **SQLAlchemy** with Snowflake dialect (`snowflake-sqlalchemy`).
- **dotenv** for managing environment variables securely.

## ⚙️ Environment Variables

Create a `.env` file in your project directory with the following content:

```ini
SNOWFLAKE_ACCOUNT=your_account_name
SNOWFLAKE_USER=your_username
SNOWFLAKE_WAREHOUSE=your_warehouse
SNOWFLAKE_DATABASE=SANDBOX
SNOWFLAKE_SCHEMA=PERSONAL_TESTING_SPACE_PRASANNA
SNOWFLAKE_ROLE=your_role
```

## 🛠️ Usage

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

Typical dependencies:
```bash
mcp
sqlalchemy
snowflake-sqlalchemy
python-dotenv
```

2. Run the MCP agent:

```bash
python your_script.py
```

The agent will start and register itself with the MCP server using `stdio` transport.

## 🧑‍💻 How It Works

- When invoked via MCP, the agent will accept a `query` parameter and optionally `database` and `schema` values.
- It will then connect to Snowflake and execute the provided query.
- The results will be returned as a JSON object, either as rows (for `SELECT` queries) or as an execution confirmation (for `INSERT/UPDATE/DELETE` queries).

## 🔄 Example Request via MCP

```json
{
  "tool": "execute",
  "params": {
    "query": "SELECT * FROM MY_TABLE LIMIT 10",
    "database": "MY_DATABASE",
    "schema": "MY_SCHEMA"
  }
}
```

## 📦 Output Example

```json
{
  "results": [
    {"COLUMN1": "value1", "COLUMN2": "value2"},
    {"COLUMN1": "value3", "COLUMN2": "value4"}
  ]
}
```

Or for non-SELECT queries:

```json
{
  "results": {
    "rowcount": 1,
    "message": "Query executed successfully"
  }
}
```

## 📚 Resources

- 📝 [MCP Servers GitHub Repository](https://github.com/modelcontextprotocol/servers/tree/main)
- ❄️ [Snowflake SQLAlchemy Documentation](https://docs.snowflake.com/en/developer-guide/sqlalchemy)

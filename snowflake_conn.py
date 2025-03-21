import os
from typing import Any, Dict
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.pool import QueuePool
from mcp.server.fastmcp import FastMCP
from snowflake.sqlalchemy import URL

# Load environment variables
load_dotenv()

mcp = FastMCP('snowflake')

# Configure SQLAlchemy engine with connection pooling for Snowflake
def create_db_engine(database: str = None, schema: str = None):
    """Create a SQLAlchemy engine for Snowflake connection.
    
    Args:
        database: Name of the database to connect to (defaults to SANDBOX)
        schema: Name of the schema to use (defaults to PERSONAL_TESTING_SPACE_PRASANNA)
    """
    account = os.getenv('SNOWFLAKE_ACCOUNT')
    user = os.getenv('SNOWFLAKE_USER')
    warehouse = os.getenv('SNOWFLAKE_WAREHOUSE')
    
    # Use provided database/schema or defaults from environment
    database = database or os.getenv('SNOWFLAKE_DATABASE')
    schema = schema or os.getenv('SNOWFLAKE_SCHEMA')
    
    # Create connection URL with external browser authentication
    connect_args = {
        'warehouse': warehouse,
        'role': os.getenv('SNOWFLAKE_ROLE'),
        'authenticator': 'externalbrowser',  # Using external browser authentication
        'database': database,
        'schema': schema
    }
    
    # Construct Snowflake connection URL
    db_url = URL(
        account=account,
        user=user,
        **connect_args
    )
    
    print(f"Connecting to Snowflake with URL: {db_url}")  # Debug print
    
    return create_engine(
        db_url,
        poolclass=QueuePool,
        pool_size=5,
        max_overflow=10,
        pool_timeout=30,
        pool_recycle=1800  # Recycle connections after 30 minutes
    )

@mcp.tool()
async def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """Execute a SQL query on the specified Snowflake database.
    
    Args:
        params: Dictionary containing:
            - query: SQL query to execute
            - database: Name of the database to query (optional)
            - schema: Name of the schema to use (optional)
    
    Returns:
        Dictionary containing query results or error message
    """
    try:
        # Extract parameters
        query = params.get('query')
        if not query:
            return {'error': 'Query parameter is required'}
            
        database = params.get('database')
        schema = params.get('schema')
        
        print(f"Executing query: {query}")  # Debug print
        print(f"Database: {database}")  # Debug print
        print(f"Schema: {schema}")  # Debug print
        
        # Create engine for the specified database
        engine = create_db_engine(database, schema)
        
        # Execute query
        with engine.connect() as conn:
            # Start a transaction
            with conn.begin():
                result = conn.execute(text(query))
                if result.returns_rows:
                    # Convert result to list of dicts
                    columns = result.keys()
                    rows = [dict(zip(columns, row)) for row in result.fetchall()]
                    return {'results': rows}
                else:
                    # For non-SELECT queries (INSERT, UPDATE, etc.)
                    return {
                        'results': {
                            'rowcount': result.rowcount,
                            'message': 'Query executed successfully'
                        }
                    }
                
    except Exception as e:
        print(f"Error occurred: {str(e)}")  # Debug print
        return {
            'error': str(e)
        }
    finally:
        # Dispose of the engine to close all connections in the pool
        if 'engine' in locals():
            engine.dispose()

if __name__ == "__main__":
   mcp.run(transport='stdio')
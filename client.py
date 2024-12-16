from gql import Client
from gql.transport.requests import RequestsHTTPTransport
from typing import Optional

def get_client(url: str, token: Optional[str] = None) -> Client:
    """
    Create and configure the GraphQL client with proper transport settings
    
    Args:
        url (str): The GraphQL endpoint URL
        token (str, optional): The bearer token for authentication
    
    Returns:
        Client: Configured GQL client instance
        
    Raises:
        ValueError: If no token is provided
    """
    if not token:
        raise ValueError("Authentication token is required")
        
    transport = RequestsHTTPTransport(
        url=url,
        headers={'Authorization': f'Bearer {token}'}
    )
    
    return Client(transport=transport, fetch_schema_from_transport=True) 
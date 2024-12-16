from gql import gql
from typing import Dict, Any

template_query = gql("""
    query GetTemplateSerializedConfig($code: String!) {
        template(code: $code) {
            id
            serializedConfig
        }
    }
""")

def get_template(client: Any, code: str) -> Dict:
    """
    Get template configuration from Railway
    
    Args:
        client: The GraphQL client
        code (str): Template code to fetch
        
    Returns:
        Dict: Template data containing id and serialized configuration
    """
    result = client.execute(template_query, variable_values={"code": code})
    return result['template'] 
from gql import gql
from typing import Dict, Any

project_create_mutation = gql("""
    mutation CreateProject($input: ProjectCreateInput!) {
        projectCreate(input: $input) {
            id
            name
            environments(first: 1) {
                edges {
                    node {
                        id
                    }
                }
            }
        }
    }
""")

def create_project(client: Any, name: str, description: str, team_id: str = None) -> Dict:
    """
    Create a new project in Railway
    
    Args:
        client: The GraphQL client
        name (str): Name of the project
        description (str): Project description
        team_id (str, optional): Team ID to create the project under
        
    Returns:
        Dict: Project creation result containing project and environment IDs
    """
    project_input = {
        "input": {
            "name": name,
            "description": description,
            "teamId": team_id
        }
    }
    
    result = client.execute(project_create_mutation, variable_values=project_input)
    return result['projectCreate'] 
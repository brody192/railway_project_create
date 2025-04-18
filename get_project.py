from gql import gql
from typing import Dict, Any, List

project_query = gql("""
    query project($projectId: String!) {
        project(id: $projectId) {
            services {
                edges {
                    node {
                        deployments {
                            edges {
                                node {
                                    status
                                }
                            }
                        }
                        id
                        templateServiceId
                    }
                }
            }
        }
    }
""")

def get_project_services_from_template(client: Any, project_id: str, template_config: Dict) -> List[Dict]:
    """
    Get services for a specific project from Railway, filtered to only include services
    that match the template configuration.
    
    Args:
        client: The GraphQL client
        project_id (str): ID of the project to query
        template_config (Dict): Template configuration containing valid service IDs
        
    Returns:
        List[Dict]: List of services with their template service IDs and IDs
    """
    # Get valid template service IDs
    valid_template_ids = set(template_config['services'].keys())
    
    variables = {
        "projectId": project_id
    }
    
    result = client.execute(project_query, variable_values=variables)
    services = result['project']['services']['edges']
    
    # Filter services to only include those with valid template IDs
    filtered_services = [
        edge['node'] for edge in services 
        if edge['node']['templateServiceId'] in valid_template_ids
    ]
    
    return filtered_services 
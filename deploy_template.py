from gql import gql
from typing import Dict, Any

deploy_mutation = gql("""
    mutation DeployTemplate($input: TemplateDeployV2Input!) {
        templateDeployV2(input: $input) {
            projectId
        }
    }
""")

def deploy_template(
    client: Any,
    serialized_config: Dict,
    template_id: str,
    project_id: str,
    environment_id: str,
    team_id: str
) -> Dict:
    """
    Deploy a template to Railway
    
    Args:
        client: The GraphQL client
        serialized_config (Dict): The template's serialized configuration
        template_id (str): ID of the template to deploy
        project_id (str): ID of the project to deploy to
        environment_id (str): ID of the environment to deploy to
        team_id (str): ID of the team to deploy under
        
    Returns:
        Dict: Deployment result containing project ID
    """
    deploy_input = {
        "input": {
            "serializedConfig": serialized_config,
            "templateId": template_id,
            "projectId": project_id,
            "environmentId": environment_id,
            "teamId": team_id
        }
    }
    
    result = client.execute(deploy_mutation, variable_values=deploy_input)
    return result['templateDeployV2'] 
from gql import gql
from typing import Dict, Any, List
import threading
from utils import get_repo_service_ids

deployment_trigger_create_mutation = gql("""
    mutation deploymentTriggerCreate($environmentId: String!, $projectId: String!, $repository: String!, $serviceId: String!, $provider: String!, $rootDirectory: String!, $branch: String!) {
        deploymentTriggerCreate(
            input: {
                environmentId: $environmentId,
                projectId: $projectId,
                repository: $repository,
                serviceId: $serviceId,
                provider: $provider,
                rootDirectory: $rootDirectory,
                branch: $branch
            }
        ) {
            id
        }
    }
""")

def create_deployment_trigger(
    client: Any,
    environment_id: str,
    project_id: str,
    repository: str,
    service_id: str,
    root_directory: str,
    branch: str
) -> Dict:
    """
    Create a deployment trigger in Railway
    
    Args:
        client: The GraphQL client
        environment_id (str): ID of the environment
        project_id (str): ID of the project
        repository (str): Repository URL or identifier
        service_id (str): ID of the service
        root_directory (str): Root directory path
        branch (str): Branch name
        
    Returns:
        Dict: Deployment trigger creation result containing trigger ID
    """
    # Set root directory to "/" if it's null
    if root_directory is None:
        root_directory = "/"
        
    trigger_input = {
        "environmentId": environment_id,
        "projectId": project_id,
        "repository": repository,
        "serviceId": service_id,
        "provider": "github",
        "rootDirectory": root_directory,
        "branch": branch
    }
    
    result = client.execute(deployment_trigger_create_mutation, variable_values=trigger_input)
    return result['deploymentTriggerCreate']

def create_deployment_triggers(
    client: Any,
    environment_id: str,
    project_id: str,
    serialized_config: Dict,
    project_services: List[Dict]
) -> List[Dict]:
    """
    Create deployment triggers for all repo-based services in the project
    
    Args:
        client: The GraphQL client
        environment_id (str): ID of the environment
        project_id (str): ID of the project
        serialized_config (Dict): The template's serialized configuration
        project_services (List[Dict]): List of services in the project with their template service IDs and IDs
        
    Returns:
        List[Dict]: List of deployment trigger creation results
    """
    triggers = []
    threads = []
    
    # Create a mapping of template service IDs to project service IDs
    service_id_map = {
        service['templateServiceId']: service['id']
        for service in project_services
    }
    
    # Find all repo-based services in the serialized config
    for template_service_id, service_info in serialized_config['services'].items():
        if 'source' in service_info and 'repo' in service_info['source']:
            # Get the project service ID for this template service
            project_service_id = service_id_map.get(template_service_id)
            if not project_service_id:
                continue
                
            # Get repository and branch info
            repo = service_info['source'].get('ogRepo', service_info['source']['repo'])
            branch = service_info['source'].get('branch', 'main')
            root_directory = service_info['source'].get('rootDirectory', '/')
            
            # Create a thread for each trigger
            thread = threading.Thread(
                target=lambda: triggers.append(
                    create_deployment_trigger(
                        client=client,
                        environment_id=environment_id,
                        project_id=project_id,
                        repository=repo,
                        service_id=project_service_id,
                        root_directory=root_directory,
                        branch=branch
                    )
                )
            )
            thread.start()
            threads.append(thread)
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    if len(triggers) != len(get_repo_service_ids(serialized_config)):
        raise Exception("Deployment triggers created does not match the number of repo-based services in the template")
    
    return triggers
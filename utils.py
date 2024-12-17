def update_service_repo(serialized_config, service_name, new_repo):
    """
    Update the repository URL for a specific service in the serialized config.
    
    Args:
        serialized_config (dict): The template's serialized configuration
        service_name (str): The name of the service to update
        new_repo (str): The new repository URL
    
    Returns:
        dict: Updated serialized config
        
    Raises:
        ValueError: If the service is not found or if the service doesn't have a repository configuration
    """
    for service_id, service_info in serialized_config['services'].items():
        if service_info.get('name') == service_name:
            if not ('source' in service_info and 'repo' in service_info['source']):
                raise ValueError(f"Service '{service_name}' exists but does not have a repository configuration")
            service_info['source']['repo'] = new_repo
            return serialized_config
    
    raise ValueError(f"Service '{service_name}' not found in config")

def update_service_name(serialized_config, old_name, new_name):
    """
    Update the name of a specific service in the serialized config.
    
    Args:
        serialized_config (dict): The template's serialized configuration
        old_name (str): The current name of the service
        new_name (str): The new name for the service
    
    Returns:
        dict: Updated serialized config
    """
    for service_id, service_info in serialized_config['services'].items():
        if service_info.get('name') == old_name:
            service_info['name'] = new_name
            return serialized_config
    
    raise ValueError(f"Service '{old_name}' not found in config")

def print_services(serialized_config: dict) -> None:
    """
    Print information about services that will be deployed
    
    Args:
        serialized_config (dict): The template's serialized configuration
    """
    services = serialized_config['services']
    print("\nServices being deployed:")
    for service_id, service_info in services.items():
        print(f"\n- {service_info.get('name', 'Unnamed Service')}:")
        if 'source' in service_info:
            if 'image' in service_info['source']:
                print(f"  Image: {service_info['source']['image']}")
            if 'repo' in service_info['source']:
                print(f"  Repo: {service_info['source']['repo']}") 
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

def enable_serverless(serialized_config, service_names):
    """
    Enable serverless mode for one or more services in the serialized config.
    
    Args:
        serialized_config (dict): The template's serialized configuration
        service_names (str or list): Single service name or array of service names to enable serverless mode for
    
    Returns:
        dict: Updated serialized config
        
    Raises:
        ValueError: If any of the services are not found
    """
    # Convert single service name to list for consistent handling
    if isinstance(service_names, str):
        service_names = [service_names]
    
    # First validate all services exist
    not_found = []
    for service_name in service_names:
        found = False
        for service_info in serialized_config['services'].values():
            if service_info.get('name') == service_name:
                found = True
                break
        if not found:
            not_found.append(service_name)
    
    if not_found:
        raise ValueError(f"Services not found in config: {', '.join(not_found)}")
    
    # If all services exist, then enable serverless mode
    for service_name in service_names:
        for service_info in serialized_config['services'].values():
            if service_info.get('name') == service_name:
                if 'deploy' not in service_info:
                    service_info['deploy'] = {}
                service_info['deploy']['sleepApplication'] = True
                break
    
    return serialized_config

def get_all_service_names(serialized_config):
    """
    Get all service names from the serialized configuration.
    
    Args:
        serialized_config (dict): The template's serialized configuration
    
    Returns:
        list: Array of all service names
    """
    return [service_info.get('name') 
            for service_info in serialized_config['services'].values() 
            if service_info.get('name') is not None]

def set_upstream_url_null(serialized_config, service_name):
    """
    Set the source.upstreamUrl to null for a specific service in the serialized config.
    Service must have a source.repo field for this operation to be valid.
    
    Args:
        serialized_config (dict): The template's serialized configuration
        service_name (str): The name of the service to update
    
    Returns:
        dict: Updated serialized config
        
    Raises:
        ValueError: If the service is not found or if service doesn't have a repo configuration
    """
    for service_id, service_info in serialized_config['services'].items():
        if service_info.get('name') == service_name:
            if not ('source' in service_info and 'repo' in service_info['source']):
                raise ValueError(f"Service '{service_name}' exists but does not have a repository configuration")
            service_info['source']['upstreamUrl'] = None
            return serialized_config
    
    raise ValueError(f"Service '{service_name}' not found in config") 
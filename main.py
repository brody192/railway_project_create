import os
from utils import update_service_repo, update_service_name, print_services
from client import get_client
from project_create import create_project
from get_template import get_template
from deploy_template import deploy_template

client = get_client(
    url='https://backboard.railway.app/graphql/v2',
    token=os.getenv("RAILWAY_API_TOKEN")
)

try:
    # Create the project
    project_result = create_project(
        client=client,
        name="Panera Project", # Replace with the name of the project
        description="A project for Panera Bread redirect service", # Replace with the description of the project
        team_id=os.getenv("RAILWAY_TEAM_ID", None)
    )
    
    # Get the template configuration
    template_result = get_template(
        client=client,
        code="JvBfQD" # Replace with your actual code
    )
    serialized_config = template_result['serializedConfig']
    
    # Update the repository URL for a service
    serialized_config = update_service_repo(
        serialized_config,
        service_name="hello-world", # Replace with the service name you want to update
        new_repo="https://github.com/brody192/302-redir" # Replace with the new repository URL
    )
    
    # Update the name of a service
    serialized_config = update_service_name(
        serialized_config,
        old_name="hello-world", # Replace with the old service name
        new_name="panera-bread" # Replace with the new service name
    )
    
    # Deploy the template
    deploy_result = deploy_template(
        client=client,
        serialized_config=serialized_config,
        template_id=template_result['id'],
        project_id=project_result['id'],
        environment_id=project_result['environments']['edges'][0]['node']['id'],
        team_id=os.getenv("RAILWAY_TEAM_ID", None)
    )

    # Print the new project's URL
    print(f"\nProject URL: https://railway.app/project/{deploy_result['projectId']}")
    
    # Print information about the services being deployed
    print_services(serialized_config)

except Exception as e:
    print(f"An error occurred: {str(e)}")
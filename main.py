import os, json
from utils import update_service_repo, update_service_name, print_services, enable_serverless, get_all_service_names, set_upstream_url_null
from client import get_client
from project_create import create_project
from get_template import get_template
from deploy_template import deploy_template

client = get_client(
    url='https://backboard.railway.app/graphql/v2',
    token=os.getenv("RAILWAY_API_TOKEN")
)

try:
    # Get the template configuration
    template_result = get_template(
        client=client,
        code="JvBfQD" # Replace with your actual code
    )
    serialized_config = template_result['serializedConfig']
    
    # Example (Optional) - Update the repository URL for a service
    serialized_config = update_service_repo(
        serialized_config,
        service_name="hello-world", # Replace with the service name you want to update
        new_repo="https://github.com/brody192/302-redir" # Replace with the new repository URL
    )
    
    # Example (Optional) - Update the name of a service
    serialized_config = update_service_name(
        serialized_config,
        old_name="hello-world", # Replace with the old service name
        new_name="panera-bread" # Replace with the new service name
    )

    # Example (Optional) - Set the upstream URL to null for a service
    serialized_config = set_upstream_url_null(
        serialized_config,
        service_name="panera-bread" # Replace with the service name you want to update
    )

    # Example (Optional) - Enable serverless mode on a single service
    serialized_config = enable_serverless(serialized_config, "panera-bread")

    # Example (Optional) - Enable serverless mode on just the databases
    # serialized_config = enable_serverless(serialized_config, ["Redis", "Postgres"])

    # Example (Optional) - Enable serverless mode on all services
    # serialized_config = enable_serverless(serialized_config, get_all_service_names(serialized_config))

    with open('template_config.json', 'w') as f:
        json.dump(serialized_config, f, indent=2)

    # Create the project
    project_result = create_project(
        client=client,
        name="Panera Project", # Replace with the name of the project
        description="A project for Panera Bread redirect service", # Replace with the description of the project
        team_id=os.getenv("RAILWAY_TEAM_ID", None)
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

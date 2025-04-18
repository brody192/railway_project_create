import os
from utils import update_service_repo, update_service_name, print_services, enable_serverless, update_repo_urls_to_default_branch, wait_for_services
from client import get_client
from project_create import create_project
from get_template import get_template
from deploy_template import deploy_template
from deployment_trigger_create import create_deployment_triggers
from get_available_github_repos import get_available_github_repos

client = get_client(
    url='https://backboard.railway.app/graphql/v2',
    token=os.getenv("RAILWAY_API_TOKEN")
)

try:
    print("Getting template configuration...")

    # Get the template configuration
    template_result = get_template(
        client=client,
        code="JvBfQD" # Replace with your actual code
    )

    serialized_config = template_result['serializedConfig']

    print("Template configuration retrieved!")

    print("Making changes to template configuration...")
    
    # Example (Optional) - Update the repository URL for a service
    serialized_config = update_service_repo(
        serialized_config,
        service_name="hello-world", # Replace with the service name you want to update
        new_repo="brody192/302-redir" # Replace with the new repository URL
    )
    
    # Example (Optional) - Update the name of a service
    serialized_config = update_service_name(
        serialized_config,
        old_name="hello-world", # Replace with the old service name
        new_name="panera-bread" # Replace with the new service name
    )

    # Example (Optional) - Enable serverless mode on a single service
    serialized_config = enable_serverless(serialized_config, "panera-bread")

    # Example (Optional) - Enable serverless mode on just the databases
    # serialized_config = enable_serverless(serialized_config, ["Redis", "Postgres"])

    # Example (Optional) - Enable serverless mode on all services
    # serialized_config = enable_serverless(serialized_config, get_all_service_names(serialized_config))

    print("Template configuration updated!")

    print("Updating repository URLs to default branch...")

    # This will cause the deployed repo based services to not have an upstream, as if they weren't deployed from a template
    serialized_config = update_repo_urls_to_default_branch(serialized_config, get_available_github_repos(client))

    print("Repository URLs updated!")

    print("Creating project...")

    # Create the project
    project_result = create_project(
        client=client,
        name="Panera Project", # Replace with the name of the project
        description="A project for Panera Bread redirect service", # Replace with the description of the project
        team_id=os.getenv("RAILWAY_TEAM_ID", None)
    )

    # Print the new project's URL
    print(f"Project URL: https://railway.com/project/{project_result['id']}")

    print("Project created!")

    print("Deploying Template...")

    # Deploy the template
    deploy_result = deploy_template(
        client=client,
        serialized_config=serialized_config,
        template_id=template_result['id'],
        project_id=project_result['id'],
        environment_id=project_result['environments']['edges'][0]['node']['id'],
        team_id=os.getenv("RAILWAY_TEAM_ID", None)
    )
    
    print("Template deploy initiated!")

    print("Waiting for services to exist...")

    template_services = wait_for_services(client, project_result['id'], serialized_config)

    print("Services exist!")

    print("Creating deployment triggers...")

    # Create the deployment triggers
    # This will create a deployment trigger for each service that is deployed from a repo
    # Aka each service will automatically deploy when the repo is pushed to
    deployment_triggers = create_deployment_triggers(
        client=client,
        environment_id=project_result['environments']['edges'][0]['node']['id'],
        project_id=project_result['id'],
        serialized_config=serialized_config,
        project_services=template_services
    )

    print("Deployment triggers created!")

    # Print information about the services being deployed
    print_services(serialized_config)

except Exception as e:
    print(f"An error occurred: {str(e)}")

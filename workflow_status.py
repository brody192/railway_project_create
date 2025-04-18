from gql import gql
from typing import Dict, Any

workflow_status_query = gql("""
    query workflowStatus($workflowId: String!) {
        workflowStatus(workflowId: $workflowId) {
            error
            status
        }
    }
""")

def get_workflow_status(client: Any, workflow_id: str) -> Dict:
    """
    Get the status of a workflow in Railway
    
    Args:
        client: The GraphQL client
        workflow_id (str): ID of the workflow to check
        
    Returns:
        Dict: Workflow status containing error and status information
    """
    result = client.execute(workflow_status_query, variable_values={"workflowId": workflow_id})
    return result['workflowStatus'] 
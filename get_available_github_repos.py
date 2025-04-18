from gql import gql
from typing import Dict, Any, List

github_repos_query = gql("""
    query getAvailableGitHubRepos {
        githubRepos {
            id
            name
            fullName
            installationId
            defaultBranch
            isPrivate
        }
    }
""")

def get_available_github_repos(client: Any) -> List[Dict]:
    """
    Get available GitHub repositories from Railway
    
    Args:
        client: The GraphQL client
        
    Returns:
        List[Dict]: List of GitHub repositories with their details
    """
    result = client.execute(github_repos_query)
    return result['githubRepos'] 
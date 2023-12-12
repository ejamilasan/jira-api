import logging
import os
from atlassian import Jira

# logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logging.getLogger("atlassian.jira").setLevel(logging.ERROR)


def jira_conn():
    return Jira(
        url=os.getenv("JIRA_URL"),
        username=os.getenv("JIRA_USERNAME"),
        password=os.getenv("JIRA_TOKEN"),
        cloud=True,
    )


def create_jira_issue(projectKey, summary, description, issueType, labels=[]):
    jira = jira_conn()

    new_issue = jira.create_issue(
        fields={
            "project": {"key": projectKey},
            "summary": summary,
            "description": description,
            "issuetype": {"name": issueType},
            "labels": labels,
        }
    )

    logger.info(f'New Jira Ticket Created: {new_issue["key"]}')

    return new_issue["key"]


def check_jira_issue_status(issue_key):
    jira = jira_conn()

    issue = jira.get_issue(issue_key)
    status = issue["fields"]["status"]["name"]

    return status

if __name__ == "__main__":
    # run function here
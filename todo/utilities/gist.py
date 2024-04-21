import os
import requests
from dotenv import load_dotenv
load_dotenv()
# Load environment variables from .env file
load_dotenv()

def export_project_summary_as_gist(project_title, todo_list):
    # Gather project summary data and format as Markdown
    markdown_content = f"# {project_title}\n\n"
    completed_task = f"## Completed\n\n"
    pending_task = f"## Pending\n\n"
    
    total_task = len(todo_list)
    total_completed=0
    # import pdb;pdb.set_trace();

    for todo in todo_list:
        if todo.status =="completed":
            check_box = "- [x]"
            completed_task+= f"{check_box} **{todo.description}** \n"
            total_completed+=1
        else:
            check_box = "- [ ]"
            pending_task += f"{check_box} **{todo.description}** \n"
    summary =  f"## Summary: {total_completed}/{total_task}: todos Coompleted \n\n"
    markdown_content += f"{summary}{completed_task} \n {pending_task}\n"

    # Prepare data for GitHub API
    github_token =  os.getenv('GITHUB_ACCESS_TOKEN')
    print(github_token)
    headers = {'Authorization': f'token {github_token}'}
    payload = {
        'description': f'Project Summary: {project_title}',
        'public': False,  # Create a secret gist
        'files': {
            'summary.md': {
                'content': markdown_content
            }
        }
    }

    # Create secret gist using GitHub API
    response = requests.post('https://api.github.com/gists', headers=headers, json=payload)
    if response.status_code == 201:
        # Save gist content to local Markdown file
        gist_data = response.json()
        gist_id = gist_data['id']
        gist_content = requests.get(gist_data['files']['summary.md']['raw_url']).text
        with open(f'{project_title}_summary.md', 'w') as file:
            file.write(gist_content)
        return f"Gist created successfully: https://gist.github.com/{gist_id}"
    else:
        return "Failed to create gist. Check your GitHub Personal Access Token and permissions."
import requests
import json
import argparse
import sys
import time

bitbucket_url = 'http://localhost'
bitbucket_port = ':7990'
api = '/rest/api/1.0/'
#token = 'MjUyMzA2Mjk1Mzc5OotzA5mBChu6VVD0dG6xSp+WCHZ7'

def get_repos_in_proj(project, api_key):
    URL = bitbucket_url + bitbucket_port + api + 'projects/' + project + '/repos'
    PARAMS = 'Authorization: Bearer '
    r = requests.get(url = URL, headers = {"Authorization": 'Bearer '+ api_key})
    data = r.json()  
    repo_slugs = []
    data = (data["values"])
    for e in data:
      repo_slugs.append(e['slug'])
      print(e['slug'])
    return repo_slugs

def prompt_question(question):
    while "the answer is invalid":
        reply = str(input(question+' (y/n): ')).lower().strip()
        if reply[:1] == 'y':
            return True
        if reply[:1] == 'n':
            return False

def remove_repos(project, repos, api_key):
  URL = bitbucket_url + bitbucket_port + api + 'projects/' + project + '/repos/'
  for repo in repos:
    r = requests.delete(url= URL + repo, headers = {"Authorization": 'Bearer '+ api_key})
    time.sleep(0.5)
    print(f"While removing. Got {r.status_code} For repo: aginst URL: {URL}")
  
def create_repos(project, repos, api_key):
  print("Recreating repos")
  URL = bitbucket_url + bitbucket_port + api + 'projects/' + 'ABC' + '/repos/'
  
  for repo in repos:
    dyn_data = '{"name": \"' + repo + '\","scmId": "git","forkable": true}'
    r = requests.post(url= URL, headers = {"Authorization": 'Bearer '+ api_key, "Content-Type": 'application/json'}, data=dyn_data)
    time.sleep(0.5)
    print(f"While creating. Got {r.status_code} For repo: aginst URL: {URL}")

def main(): 
  args = parser.parse_args()
  check_args(args)

  project = args.project
  api_key = args.api_key

  repos = get_repos_in_proj(project, api_key)
  delete_repos = prompt_question("Would you like to remove theese repos?")
  if delete_repos:
    recreate_repos = prompt_question("Would you like to recreate these repos but empty?")
  if(delete_repos):
    remove_repos(project, repos, api_key)
  if(recreate_repos):
    create_repos(project, repos, api_key)

def check_args(args):
  if not args.project:
    sys.exit("Please add project")
  if not args.api_key:
    sys.exit("Please add api-key")


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description="Set project and api-key")
  parser.add_argument("-p", "--project", help="Specify project name (slug)")
  parser.add_argument("-k", "--api-key", help="Specify api-key")
  main()
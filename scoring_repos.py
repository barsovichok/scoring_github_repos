import requests
from datetime import datetime


def get_repo_json(repo_params, user):
    url = f'https://api.github.com/repos/{user}'
    result = requests.get(url, params=repo_params).json()
    return result


def get_repo_resource_json(repo_resource, repo_params, user):
    url = f'https://api.github.com/repos/{user}{repo_resource}'
    result = requests.get(url, params=repo_params).json()
    return result


def get_repo_contributors(repo_contributors_json):
    repo_contributors = len(repo_contributors_json)
    return repo_contributors


def get_repo_pull_requests(repo_pull_requests_json, date_offset):
    pull_requests = []

    for request in repo_pull_requests_json:
        list_repo = str(request['merged_at'])
        list_repo = list_repo[:date_offset]
        pull_requests.append(list_repo)

    for pr in pull_requests:
        if pr == 'None':
            pull_requests.remove(pr)

    return pull_requests


def get_repo_file(repo_files_json):
    repo_files = []
    for file_name in repo_files_json:
        list_repo_file = file_name['name']
        repo_files.append(list_repo_file)

    return repo_files


def get_pull_requests_date_delta(pull_requests):
    date_request = []
    repo_delta = []
    count_delta = []

    for pull_request in pull_requests:
        pull_request = datetime.strptime(pull_request, '%Y-%m-%d')
        date_request.append(pull_request)

    now = datetime.today()

    for date in date_request:
        delta = now - date
        delta = delta.days
        repo_delta.append(delta)

    repo_delta.sort()

    for r_delta in repo_delta:
        
        if r_delta < 30:
            count_delta.append(r_delta)

    pull_request_number = len(count_delta)
    return pull_request_number
    


def count_repo_result(repo_files, repo_contributors,
                      pull_requests, repo_readme_json, repo_json, pull_request_number):

    repo_result = 0

    if pull_request_number != 0:
        repo_result += 1

    if '.editorconfig' in repo_files:
        repo_result += 1

    if '.travis.yml' in repo_files:
        repo_result += 1

    if repo_contributors > 10:
        repo_result += 2

    elif 2 < repo_contributors < 10:
        repo_result += 1

    if 'name' in repo_readme_json.keys():
        repo_result += 1

    if repo_json['license'] is not None:
        repo_result += 1

    if repo_json['forks'] != 0:
        repo_result += 1

    if repo_json['stargazers_count'] > 50:
        repo_result += 2

    elif 1 < repo_json['stargazers_count'] < 50:
        repo_result += 1

    return repo_result


def print_repo_result(repo_result):
    print("Оценка репо: " + str(repo_result))

    

date_offset = 10

repo_params = {
    'client_id': 'bb075a31f15f7f7354df',
    'client_secret': 'bba1541f020e844333036e1959312ac5b1a9380e',
}

if __name__ == '__main__':
    user = input('Укажите репозиторий в формате owner/repo\n')

    repo_contributors_json = get_repo_resource_json(
        user=user,
        repo_resource='/contributors',
        repo_params=repo_params,
    )

    repo_readme_json = get_repo_resource_json(
        user=user,
        repo_resource='/readme',
        repo_params=repo_params,
    )

    repo_pull_requests_json = get_repo_resource_json(
        user=user,
        repo_resource='/pulls',
        repo_params=repo_params.update({'state': 'all'}),
    )

    repo_files_json = get_repo_resource_json(
        user=user,
        repo_resource='/contents',
        repo_params=repo_params,
    )

    repo_json = get_repo_json(
        user=user,
        repo_params=repo_params,
    )

repo_contributors = get_repo_contributors(repo_contributors_json)
pull_requests = get_repo_pull_requests(repo_pull_requests_json,date_offset)
pull_request_number = get_pull_requests_date_delta(pull_requests)
repo_files = get_repo_file(repo_files_json)
repo_result = count_repo_result(
    repo_files,
    repo_contributors,
    pull_requests,
    repo_readme_json,
    repo_json,
    pull_request_number
)
print_repo_result(repo_result)

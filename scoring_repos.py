import requests
from datetime import datetime
import os

date_delta = 30

REPO_PARAMS = {
        'client_id': os.environ.get('client_id'),
        'client_secret':  os.environ.get('client_secret'),
    }


REPO_PULL_PARAMS = {
        'client_id': os.environ.get('client_id'),
        'client_secret':  os.environ.get('client_secret'),
        'state': 'all',
    }


def get_repository():
    repository = input('Укажите репозиторий в формате owner/repo\n')
    return repository


def return_repo_params():
    return REPO_PARAMS


def return_repo_pull_params():
    return REPO_PULL_PARAMS


def check_user_input(repository):
    url = f'https://api.github.com/repos/{repository}'
    result = requests.get(url, params=REPO_PARAMS).json()
    if result.get('message') == 'Not Found':
        return None
    else:
        return result


def get_repo_json(repo_params, repository):
    url = f'https://api.github.com/repos/{repository}'
    result = requests.get(url, params=REPO_PARAMS).json()

    return result


def get_repo_resource_json(repo_resource, repo_params, repository):
    url = f'https://api.github.com/repos/{repository}{repo_resource}'
    result = requests.get(url, params=repo_params).json()

    return result


def get_repo_contributors(repo_contributors_json):
    repo_contributors = len(repo_contributors_json)
    return repo_contributors


def get_repo_pull_requests(repo_pull_requests_json):
    pull_requests = []

    for request in repo_pull_requests_json:
        list_repo = str(request['merged_at'])
        pull_requests.append(list_repo)

    return pull_requests


def get_repo_file(repo_files_json):
    repo_files = []
    for file_name in repo_files_json:
        list_repo_file = file_name['name']
        repo_files.append(list_repo_file)

    return repo_files


def get_pull_requests_date_delta(pull_requests, date_delta):

    date_request = []
    repo_delta = []
    count_delta = []

    for pull_request in pull_requests:
        if pull_request == 'None':
            pull_requests.remove(pull_request)
        else:
            pull_request = datetime.strptime(
                pull_request,
                '%Y-%m-%dT%H:%M:%SZ'
            )
            pull_request = datetime.date(pull_request)
            date_request.append(pull_request)

    now = datetime.today()
    now = datetime.date(now)

    for date in date_request:
        delta = now - date
        delta = delta.days
        repo_delta.append(delta)

    repo_delta.sort()

    for r_delta in repo_delta:
        if r_delta < date_delta:
            count_delta.append(r_delta)

    pull_request_amount = len(count_delta)
    return pull_request_amount


def count_repo_result(repo_files, repo_contributors,
                      pull_requests, repo_readme_json,
                      repo_json, pull_request_amount):

    repo_result = 0

    if pull_request_amount != 0:
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
    print('Оценка репо: ' + str(repo_result))


def eval_repository(repository):

    repo_contributors_json = get_repo_resource_json(
                repository=repository,
                repo_resource='/contributors',
                repo_params=REPO_PARAMS,
            )

    repo_readme_json = get_repo_resource_json(
                repository=repository,
                repo_resource='/readme',
                repo_params=REPO_PARAMS,
            )

    repo_pull_requests_json = get_repo_resource_json(
                repository=repository,
                repo_resource='/pulls',
                repo_params=REPO_PULL_PARAMS,
            )

    repo_files_json = get_repo_resource_json(
                repository=repository,
                repo_resource='/contents',
                repo_params=REPO_PARAMS,
            )

    repo_json = get_repo_json(
                repository=repository,
                repo_params=REPO_PARAMS,
            )

    repo_contributors = get_repo_contributors(repo_contributors_json)

    pull_requests = get_repo_pull_requests(
                repo_pull_requests_json
            )

    pull_request_amount = get_pull_requests_date_delta(
                pull_requests,
                date_delta
            )

    repo_files = get_repo_file(repo_files_json)

    repo_result = count_repo_result(
                repo_files,
                repo_contributors,
                pull_requests,
                repo_readme_json,
                repo_json,
                pull_request_amount
            )

    return repo_result


if __name__ == '__main__':

    date_delta = 30

    repository = get_repository()

    check_user_input = check_user_input(repository)

    if check_user_input is None:
        print('Повторите ввод')
    else:
        repo_result = eval_repository(repository)
        print_repo_result(repo_result)

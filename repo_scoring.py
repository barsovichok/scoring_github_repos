import requests
import config
from datetime import datetime


REPO_PARAMS = {
    'client_id': config.CLIENT_ID,
    'client_secret': config.СLIENT_SECRET
}

REPO_PULL_PARAMS = {
    'client_id': config.CLIENT_ID,
    'client_secret': config.СLIENT_SECRET,
    'state': config.STATE
}


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


def get_pull_request_amount(pull_requests, DATE_DELTA):

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
        if r_delta < DATE_DELTA:
            count_delta.append(r_delta)

    pull_request_amount = len(count_delta)
    return pull_request_amount


def count_repo_score(repo_files, repo_contributors_json,
                     pull_requests, repo_readme_json,
                     repo_json, pull_request_amount):

    repo_score = 0

    if pull_request_amount != 0:
        repo_score += 1

    if '.editorconfig' in repo_files:
        repo_score += 1

    if '.travis.yml' in repo_files:
        repo_score += 1

    if len(repo_contributors_json) > 10:
        repo_score += 2

    elif 2 < len(repo_contributors_json) < 10:
        repo_score += 1

    if 'name' in repo_readme_json.keys():
        repo_score += 1

    if repo_json['license'] is not None:
        repo_score += 1

    if repo_json['forks'] != 0:
        repo_score += 1

    if repo_json['stargazers_count'] > 50:
        repo_score += 2

    elif 1 < repo_json['stargazers_count'] < 50:
        repo_score += 1
    return repo_score


def print_repo_result():
    print(f'Оценка репо: {str(repo_score)}')
    print((f'Языки репозитория: {languages}'))
    print(f'{REPO_PARAMS}')
    print(f'{repository}')


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

    pull_requests = get_repo_pull_requests(
                repo_pull_requests_json
            )

    pull_request_amount = get_pull_request_amount(
                pull_requests,
                config.DATE_DELTA
            )

    repo_files = get_repo_file(repo_files_json)

    repo_score = count_repo_score(
                repo_files,
                repo_contributors_json,
                pull_requests,
                repo_readme_json,
                repo_json,
                pull_request_amount
            )
    return repo_score


def repository_language(repository):

    repo_languages_json = get_repo_resource_json(
                repository=repository,
                repo_resource='/languages',
                repo_params=REPO_PARAMS,
            )
    languages = list(repo_languages_json.keys())
    return languages


if __name__ == '__main__':

    repository = config.REPOSITORY

    check_user_input = check_user_input(repository)

    if check_user_input is None:
        print('Повторите ввод')
    else:
        repo_score = eval_repository(repository)
        languages = repository_language(repository)
        print_repo_result()

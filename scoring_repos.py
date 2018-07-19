import requests
from datetime import datetime


def make_repo_url(repo_params, user):
    url = f'https://api.github.com/repos/{user}'
    result = requests.get(url, params=repo_params).json()
    return result


def make_repo_resource_url(repo_resource, repo_params, user):
    url = f'https://api.github.com/repos/{user}{repo_resource}'
    result = requests.get(url, params=repo_params).json()
    return result


def get_repo_contributors(make_repo_contributor_url):
    repo_contributors = len(make_repo_contributor_url)
    return repo_contributors


def get_repo_pull_requests(make_repo_pulls_url):
    pull_requests = []

    for request in make_repo_pulls_url:
        list_repo = str(request['merged_at'])
        list_repo = list_repo[:10]
        pull_requests.append(list_repo)

    for pr in pull_requests:
        if pr == 'None':
            pull_requests.remove(pr)

    return pull_requests


def get_repo_file(make_repo_files_url):
    repo_files = []
    for file_name in make_repo_files_url:
        list_repo_file = file_name['name']
        repo_files.append(list_repo_file)

    return repo_files


def get_pull_requests_date_delta(pull_requests):
    date_request = []
    repo_delta = []

    for pull_request in pull_requests:
        pull_request = datetime.strptime(pull_request, '%Y-%m-%d')
        date_request.append(pull_request)

    now = datetime.today()

    for date in date_request:
        delta = now - date
        delta = delta.days
        repo_delta.append(delta)

    repo_delta.sort()

    return repo_delta


def count_repo_result(repo_files, repo_contributors,
                      pull_requests, repo_delta, make_repo_readme_url, repo):

    repo_result = 0

    if repo_delta != []:
        if repo_delta[0] < 30:
            repo_result += 1

    if '.editorconfig' in repo_files:
        repo_result += 1

    if '.travis.yml' in repo_files:
        repo_result += 1

    if repo_contributors > 10:
        repo_result += 2

    elif repo_contributors > 2 and repo_contributors < 10:
        repo_result += 1

    if 'name' in make_repo_readme_url.keys():
        repo_result += 1

    if repo['license'] is not None:
        repo_result += 1

    if repo['forks'] != 0:
        repo_result += 1

    if repo['stargazers_count'] > 50:
        repo_result += 2

    elif repo['stargazers_count'] > 1 and repo['stargazers_count'] < 50:
        repo_result += 1

    print("Оценка репо: " + str(repo_result))


if __name__ == '__main__':
    user = input('Укажите репозиторий в формате owner/repo\n')
    
    make_repo_contributor_url = make_repo_resource_url(
    user=user,
    repo_resource='/contributors',
    repo_params={
        'client_id': 'bb075a31f15f7f7354df',
        'client_secret': 'bba1541f020e844333036e1959312ac5b1a9380e'
        }
    )

make_repo_readme_url = make_repo_resource_url(
    user=user,
    repo_resource='/readme',
    repo_params={
        'client_id': 'bb075a31f15f7f7354df',
        'client_secret': 'bba1541f020e844333036e1959312ac5b1a9380e'
        }
    )

make_repo_pulls_url = make_repo_resource_url(
    user=user,
    repo_resource='/pulls',
    repo_params={
        'client_id': 'bb075a31f15f7f7354df',
        'client_secret': 'bba1541f020e844333036e1959312ac5b1a9380e',
        'state': 'all'
        }
    )

make_repo_files_url = make_repo_resource_url(
    user=user,
    repo_resource='/contents',
    repo_params={
        'client_id': 'bb075a31f15f7f7354df',
        'client_secret': 'bba1541f020e844333036e1959312ac5b1a9380e'
        }
    )

repo = make_repo_url(
    user=user,
    repo_params={
        'client_id': 'bb075a31f15f7f7354df',
        'client_secret': 'bba1541f020e844333036e1959312ac5b1a9380e'
        })

repo_contributors = get_repo_contributors(make_repo_contributor_url)
pull_requests = get_repo_pull_requests(make_repo_pulls_url)
repo_delta = get_pull_requests_date_delta(pull_requests)
repo_files = get_repo_file(make_repo_files_url)
count_repo_result = count_repo_result(
    repo_files,
    repo_contributors,
    pull_requests,
    repo_delta,
    make_repo_readme_url,
    repo)


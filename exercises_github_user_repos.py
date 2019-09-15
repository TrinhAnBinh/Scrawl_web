import requests
import argparse


def repositorys(user):
    '''
    return a generator of all repositorys of user from github.com/user
    '''
    url = f'https://api.github.com/users/{user}/repos'
    session = requests.Session()
    response = session.get(url)
    if response.status_code != 200:
        print("Connect Error!")
        yield {}
    else:
        yield response.json()

    while "next" in response.links:
        url = response.links.get('next').get('url')
        response = session.get(url)
        yield response.json()


def print_repositorys(user):
    repo_number = 0
    pages = repositorys(user)
    for page in pages:
        for repo in page:
            repo_number += 1
            repo_name = repo.get('name')
            repo_url = repo.get('html_url')
            print(f'{repo_number} | {repo_name} | {repo_url}')


def main():
    parser = argparse.ArgumentParser(
        description='Show all repositorys of user on github.com',
        prog='Github_user_repositorys')
    parser.add_argument("user", help="username on github.com", type=str)
    args = parser.parse_args()
    print_repositorys(args.user)


if __name__ == "__main__":
    main()

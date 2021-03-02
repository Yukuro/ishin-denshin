import requests

def notify (message, token):
    url = "https://notify-api.line.me/api/notify"
    headers = {'Authorization': f'Bearer {token}'}
    data = {'message': f'{message}'}

    requests.post(url, headers=headers, data=data)
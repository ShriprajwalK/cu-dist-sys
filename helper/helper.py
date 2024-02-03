def get_credentials(data):
    if 'body' in data and 'username' in data['body'] and 'password' in data['body']:
        return {'username': data['body']['username'], 'password': data['body']['password']}
    else:
        return False

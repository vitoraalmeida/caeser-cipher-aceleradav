import requests
import caesar_cipher
import hashlib
import json

token = 'TOKEN'
url = 'https://api.codenation.dev/v1/challenge/dev-ps/generate-data'
url_solution = 'https://api.codenation.dev/v1/challenge/dev-ps/submit-solution'
filename = 'answer.json'

def main():
    get_answer_json(url,token)
    decrypted = decrypt_message(filename)
    crypto_summary = generate_crypto_summary(decrypted)
    update_answer(filename, decrypted, crypto_summary)
    post_answer_json(url_solution, token, filename)


def get_answer_json(url, token):
    try:
        print('Trying to get the message...')
        response = requests.get(f'{url}?token={token}')
        print(type(response.text))
        data = response.json()
        with open(filename, 'w') as f:
            json.dump(data, f)

    except HTTPError as http_err:
        print(f'HTTP error ocurred: {http_err}')
    except Exception as err:
        print(f'Some error ocurred: {err}')
    else:
        print('Got it!\n')


def decrypt_message(filename):
    with open(filename, 'r') as f:
        answer = json.load(f)
        encrypted = answer['cifrado']
        shift = answer['numero_casas']
        decrypted = caesar_cipher.execute(encrypted, shift, 'decode')
    f.close()

    print(f'Encrypted text: \n\n {encrypted}\n')
    print(f'Shift: {shift}\n')
    print(f'Decrypted message: \n\n {decrypted}')

    return decrypted


def generate_crypto_summary(message):
    sha1 = hashlib.sha1()
    sha1.update(message.encode())
    crypto_summary = sha1.hexdigest()
    return crypto_summary


def update_answer(filename, message, crypto_summary):
    with open(filename, 'r+') as f:
        answer = json.load(f)
        answer['decifrado'] = message
        answer['resumo_criptografico'] = crypto_summary
        f.seek(0)
        json.dump(answer, f)
    f.close()


def post_answer_json(url, token, filename):
    try:
        print('\nTrying to submit solution...')
        response = requests.post(f'{url}?token={token}',
                                 files={"answer": open(filename, "rb")})

    except HTTPError as http_err:
        print(f'HTTP error ocurred: {http_err}')
    except Exception as err:
        print(f'Some error ocurred: {err}')
    else:
        print('\nGot it!\n')
        print(response.text)


if __name__ == "__main__":
    main()

import json
import time
import pybase64
import requests


class Text2ImageAPI:

    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_model(self):
        response = requests.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']

    def generate(self, prompt, model, images=1, width=1024, height=1024):
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": f"{prompt}"
            }
        }

        data = {
            'model_id': (None, model),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']

    def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['images']

            attempts -= 1
            time.sleep(delay)

    def b64i(self,images,img_path):
        decoded_data=pybase64.b64decode((images[0]))
        img_file = open(img_path, 'wb')
        img_file.write(decoded_data)
        img_file.close()

if __name__ == '__main__':
    api = Text2ImageAPI('https://api-key.fusionbrain.ai/', 'C18CFED3080CB4D9EA3470D44C3C7F99', '06E91E54D8F83FD78A6BFE43CD57A5A7')
    model_id = api.get_model()
    uuid = api.generate("белый котенок", model_id)
    images = api.check_generation(uuid)
    api.b64i(images,"img/vfmio.png")
#Не забудьте указать именно ваш YOUR_KEY и YOUR_SECRET.
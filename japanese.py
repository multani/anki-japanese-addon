from .lib import romkan
import json
from urllib.request import urlopen
from urllib.parse import urlencode
import boto3
import botocore.exceptions
# from PyQt5.QtNetwork import QNetworkAccessManager
# from PyQt5.QtNetwork import QNetworkRequest


class Content:
    def __init__(self, config):
        self.config = config

        aws = self.config.get("aws", {})
        self.polly_voice = aws.get("voice", "Mizuki")
        self.output_format = "mp3"
        self.jisho_api = "https://jisho.org/api/v1/search/words"

        print("Initializing AWS settings")
        aws = self.config.get("aws", {})
        kw = {
            "region_name": aws.get("region"),
            "profile_name": aws.get("profile_name"),
            "aws_access_key_id": aws.get("access_key"),
            "aws_secret_access_key": aws.get("secret_key"),
        }

        session = boto3.Session(**kw)
        self.polly = session.client("polly")

    def speak(self, value):
        try:
            response = self.polly.synthesize_speech(
                VoiceId=self.polly_voice,
                OutputFormat=self.output_format,
                Text=value,
            )
        except botocore.exceptions.BotoCoreError as exc:
            print("Unable to synthesize: {}".format(exc))
            return None, None

        # TODO: manage AWS errors while synthesizing
        return response['AudioStream'], self.output_format

    def translate(self, value):
        qs = urlencode({
            "keyword": value
        })
        url = "{}?{}".format(self.jisho_api, qs)

        u = urlopen(url)
        data = json.loads(u.read())

        if data['meta']['status'] != 200:
            # not found
            return None

        tr = data['data'][0]

        if "word" in tr["japanese"][0]:
            kanji = tr["japanese"][0]["word"]
        else:
            # when translating a katakana apparently
            kanji = ""

        senses = [
            s.strip()
            for s in tr["senses"][0]["english_definitions"]
        ]
        romaji = romkan.to_roma(value)
        original = tr["japanese"][0]["reading"]

        return {
            "kanji": kanji,
            "senses": senses,
            "romaji": romaji,
            "original": original,
        }

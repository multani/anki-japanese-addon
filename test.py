import boto3

polly_client = boto3.Session(
        profile_name="myown",
        # aws_access_key_id=,
        # aws_secret_access_key=,
        region_name='eu-west-3').client('polly')

data = 'あい'

response = polly_client.synthesize_speech(
    VoiceId='Mizuki',
    OutputFormat='mp3',
    Text=data,
)

with open('speech.mp3', 'wb') as fp:
    fp.write(response['AudioStream'].read())

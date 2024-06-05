import requests


# sk-k1T17P9dOVdkdHF1Cx03YB9uKvtitMfNs0AF0OMXzauk6Dzt

response = requests.post(
    f"https://api.stability.ai/v2beta/image-to-video",
    headers={
        "authorization": f"Bearer sk-MYAPIKEY"
    },
    files={
        "image": open("./kittens-in-space.png", "rb")
    },
    data={
        "seed": 0,
        "cfg_scale": 1.8,
        "motion_bucket_id": 127
    },
)

print("Generation ID:", response.json().get('id'))
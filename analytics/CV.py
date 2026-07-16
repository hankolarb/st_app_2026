import json
from google.cloud import vision

google_credentials = '''
{
  "type": "service_account",
  "project_id": "ttc-cloud-st-2025",
  "private_key_id": "91049cda319671140ce5d8883a7248a3df08bffe",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDiAXjUswu8Glfs\n+WkyjAjpqXLyF+AQx92zqCRbxe4fbMEw0825nAUHp9yVn3U3wIHG/SxoGR9xF/9l\nOoPVyl1Lq2FOhSthupDZdbXMcUYtnHXRdlOlWv732LN/3Cys8hnDBa/w5qSbxvIP\nQnyyuqGU9egt13YSv5jlcT7QoLnwR7N8vOfxBEWv1p5D2EwZTdTGwjxQWP+cuSSh\nA60oKn8L4yBWAiU3WRwGDOkS85N5s9vdw62zN2w3QGSutXMEo+bOiH4v02SkO+Hy\nGcecLX1rWDsF899MC7hpsnzmFRbNd8l462CclBRZReXb70vfhNUKfwioEVB7p8w8\ngkmrLTZBAgMBAAECggEAWwfWwG1hk6FUuvl2msp2qI784nAlavzl2oAmLOTbVcL7\nSYx2N4WVLRE6svVoRE2AuEKvSTqdRHMzBnX8NfdtfpYH+pV+9L0trLlRwYf6iVKU\nzgqIBHlTa0bYfe6T/BEDuV6oEDMGKEyIoQbZrS+o95PYseYwA7syfXAQqf2jBxlI\nI3LqQe67or2PA43vroaOlmkt/FoTkzKNjWbnEP844n7/egXB1EEGrwgWv7UsRNf2\nstUWi4B+5mI6bXBXgsEqFsrfRaRKemsjdioounzGv+/zWY6JXHZyIbKzZ8VmSN59\nOhllywrwpBisPoAmybaNnCQnFT5UzMcKovgJsRMbBQKBgQD/By7oENHhDmr6rdEb\nLiiplImPoR8FOvkvwxPfmvZtQpnVSISismDDt4WVj8+kaXZLUWrEaQIKNl3TvBjH\nRWDBDjZ2mAIGN9+r87BqCaKOcGnqbaH3H8XPrMHKEAG9Hn3S36PA/OypGABMyDRM\ninTXPLCYBlm6yhor7jMKdn0J4wKBgQDi3fkqgo1na0O5YGN3SIQSrgT/1x0x5BS6\n0w0TrecJ8XnraP1DlC2WhPJbNG57r3EYTccFAFGKyPb2jEU+RjvHSGJ/EXwBWBDb\nqbtQtN518PvNU6EuBLnpZWg0+Fc8fVz/wfn905ICOXi5D0P4XFUsoRJODeKpxHxD\nO8Ant0tIiwKBgQDKs3Dq7wOCeC07lhAQJH4ZW4CC8rNvOtJ4zfrrzYV0jm0rAvq5\nPkJ/DU1V9Po7Wb+2Wb4c4sHGUDP/aQ/gwxoGGD/dvzBMtPhI+eYMQiA8SslElWMY\nwt49FLjq3BIluSiVBUBo0h9gvzztymsXMy1vLkPGcbW8K4rlw+w5srfrtQKBgQCh\nzTiJBgV9zfXGP6WRDGoNvIkaQryyuX3DZQS9lVjjMZMHv6Bp00PUR0tmmvV1R0I8\n2DPqMDj3566jVpWH/aVi0xBUmg68EqgrUlmjDOxgZ5fe8BdTb9F8UXPJ25i0LqDm\nU91NF9jZt02PhwCuIIQqyVH501NmSxlpBjNc4BBUUwKBgFlLd1PLoRZvigV5cR25\nHyhbsU9sRhaMYeusqG0Hb2NtlIEN8BQeavVy3PWqBM4Bkk5KevfU1LWyWtRz3387\nSHSYzc6Zxb+e0q2TxqwmJ9uwKmEmDNs0euciBI1VT8Q3Y7BsL1ncoMFeCEMuC+Ti\nsL5dWlLlUTW3BOCQn0guSq59\n-----END PRIVATE KEY-----\n",
  "client_email": "ttc-cloud-2026@ttc-cloud-st-2025.iam.gserviceaccount.com",
  "client_id": "108673208823041273644",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/ttc-cloud-2026%40ttc-cloud-st-2025.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
'''

credentials_dict = json.loads(google_credentials, strict=False)
client = vision.ImageAnnotatorClient.from_service_account_info(info=credentials_dict)

img_path = "./people.png"
with open(img_path, "rb") as f:
    img = f.read()

image = vision.Image(content=img)
response = client.label_detection(image=image)

print(response)


import requests

headers = {
    'User-Agent': 'okhttp/3.11.0',
    'Content-Type': 'application/x-www-form-urlencoded',
    'standardua': '{"channelName":"dmkj_Android","countryCode":"CN","createTime":1758276123868,"device":"google Pixel 4","hardware":"flame","jPushId":"1507bfd3f6ff69d8819","modifyTime":1758276123868,"operator":"%E6%9C%AA%E7%9F%A5","screenResolution":"1080-2236","startTime":1758276471569,"sysVersion":"Android 29 10","system":"android","uuid":"2710bd5dee6e4ddd900fb5122cd8bb0d","version":"4.9.1"}',
}

data = {
    'd': 'bDFEM3RHQkxRZkk4Y2Mvb2ExSmUvTkthcm13OHdSZTllQVd4c1Rzb3BKVzJJ ejZSaTBTaTNTQ1M5bGorIFVXK3I1M0F6UHA4c0t6WGppdWNCMUZLN3F6dncx bkc2S0JObncyMFJCU0wrbGZEdEZEZkxjT1ROV0h3TCB4SUY5dU92TituN3lR NXFmcEE3MElHSFNVZGxhZVc1OVVnNDN4dk43aDJRVHN0RVlKSEdXQUNaSnBm aVQgQnZQMXJJLzExbXhMdzhwZ0JSUTZ6bTFOcVg4WDJxR1ppem55YTZITUpa VzB2MWI2R1FVRHFYaz1mS3pQRGU0MTVMV2hlS1RsdTFMNndmdlpkaXl6NCtN RnowSWx3cEgvUnJNTGdSd3lXZWF0Y1hIb1F2RGpCcEJGekg0bEQ1ZzBXWTQ3 WnNBMWFHcEQ1R0Uzb29Sbjh2KzQxMDk1RnNMT2tScjYwbHEwNG91Wm9jZkJR anJlTDFRMjJLNytzZDZpVzE5Y0RsdUNIYWNSRUR2aFlDSGlJcXRHMGVYbjkr ZlRITEE9',
}

response = requests.post('https://appdmkj.5idream.net/v2/login/phone', headers=headers, data=data)

print(response.json())
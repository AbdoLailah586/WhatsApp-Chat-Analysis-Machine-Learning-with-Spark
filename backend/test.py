from app.services.keyword_classifier import classify_by_keywords
test_msgs = [
    'Can you send me the report by tomorrow?',
    'Haha that meme was hilarious',
    'Mom says dinner is ready',
    'URGENT: Need the contract signed ASAP',
    '50% OFF SALE TODAY ONLY',
    'Congratulations you won an iPhone',
    'Check out this viral TikTok video',
]
for msg in test_msgs:
    result = classify_by_keywords(msg)
    print(f'{msg[:50]:<50} -> {result["category"]} ({result["confidence"]:.0f}%)')

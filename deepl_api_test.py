import deepl

auth_key = "your-deepl-api-key"  # Replace with your key
translator = deepl.Translator(auth_key)

result = translator.translate_text("Hello, world!", target_lang="zh")
print(result.text)

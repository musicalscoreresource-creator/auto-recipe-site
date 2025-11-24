import os
import openai
import yaml

LANGUAGES = {
    "en": "English",
    "de": "German",
    "es": "Spanish",
    "it": "Italian",
    "tr": "Turkish",
    "ru": "Russian",
    "zh": "Chinese",
    "ja": "Japanese",
    "zu": "Zulu"
}

openai.api_key = os.getenv("OPENAI_API_KEY")

def translate_text(text, target_language):
    prompt = f"""
    Translate the following cooking recipe into {target_language}.
    Keep the structure exactly the same.
    Do NOT add anything extra.
    Recipe:
    {text}
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message["content"]


def main():
    el_folder = "recipes/el"
    files = os.listdir(el_folder)

    for filename in files:
        if filename.endswith(".md"):
            source_path = os.path.join(el_folder, filename)

            print(f"Processing: {filename}")

            with open(source_path, "r", encoding="utf-8") as f:
                original = f.read()

            for lang_code, lang_name in LANGUAGES.items():
                dest_folder = f"recipes/{lang_code}"
                os.makedirs(dest_folder, exist_ok=True)

                dest_path = os.path.join(dest_folder, filename)

                translated = translate_text(original, lang_name)

                with open(dest_path, "w", encoding="utf-8") as f:
                    f.write(translated)

                print(f"→ Saved {lang_code}/{filename}")

    print("All translations completed.")


if __name__ == "__main__":
    main()

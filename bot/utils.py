import os
import yaml


class Provider:
    """Receives values from config or locale files"""

    DEFAULT_LOCALE = 'ru'
    LOCALES_PATH = os.path.join('templates', 'locales')

    @classmethod
    def __get_data(cls, path: str, source_file: str, value: str):
        """Protected method for retrieving data from specialized files."""
        if source_file:
            path = os.path.join(path, source_file)

        try:
            with open(path, 'r', encoding='utf-8') as f:
                response = yaml.safe_load(f)
        except Exception as e:
            return f"Error: {str(e)}"

        keys = value.split('.')

        for key in keys:
            if key.isdigit():
                key = int(key)
            response = response.get(key, None)

            if response is None:
                return 'None'

        return response

    @classmethod
    def get_text(cls, value: str, locale: str = DEFAULT_LOCALE):
        """Retrieves and returns localized text strings based on the specified language."""
        source_file = f"{locale}.yml"
        return str(cls.__get_data(cls.LOCALES_PATH, source_file, value))

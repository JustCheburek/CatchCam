import yaml
import os


def read_settings():
    path = "settings.yaml"
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def read_colors():
    path = "colors.yaml"
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def save(**settings_given):
    """Метод для сохранения настроек в YAML"""
    for key, value in settings_given.items():
        settings[key] = value
    with open("settings.yaml", "w", encoding="utf-8") as f:
        yaml.dump(settings, f, allow_unicode=True, sort_keys=False)


settings = read_settings()
colors = {}  # ЦВЕТА в BGR
for name, value in read_colors().items():
    colors[name] = tuple(value)

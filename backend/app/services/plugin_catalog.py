import yaml
from pathlib import Path
from typing import List

from app.models.plugin import Plugin, PluginListResponse, PluginStatus


PLUGINS_DIR = Path(__file__).parent.parent.parent.parent / "plugins"


def load_plugin_configs() -> List[Plugin]:
    plugins = []
    if not PLUGINS_DIR.exists():
        return plugins

    for plugin_dir in PLUGINS_DIR.iterdir():
        if not plugin_dir.is_dir():
            continue

        config_file = plugin_dir / "plugin.yaml"
        if not config_file.exists():
            continue

        try:
            with open(config_file, "r") as f:
                data = yaml.safe_load(f)

            plugin = Plugin(
                id=plugin_dir.name,
                name=data.get("name", plugin_dir.name),
                description=data.get("description", ""),
                version=data.get("version", "0.0.0"),
                author=data.get("author", "Unknown"),
                status=PluginStatus(data.get("status", "active")),
                tags=data.get("tags", []),
                repository=data.get("repository"),
                homepage=data.get("homepage"),
                license=data.get("license"),
            )
            plugins.append(plugin)
        except Exception:
            continue

    return plugins


def get_plugins() -> PluginListResponse:
    plugins = load_plugin_configs()
    return PluginListResponse(plugins=plugins, total=len(plugins))

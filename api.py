import json

from .preset_store import SettingsPresetStore


try:
    from aiohttp import web
    from server import PromptServer
except ImportError:  # pragma: no cover - only available inside ComfyUI
    web = None
    PromptServer = None


PRESET_STORE = SettingsPresetStore()
API_BASE_PATH = "/oc/settings-presets"
API_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
}
ROUTES_REGISTERED = False


def json_response(payload, status=200):
    if web is None:
        return None
    return web.json_response(payload, status=status, headers=API_HEADERS)


def register_routes():
    global ROUTES_REGISTERED

    if web is None or PromptServer is None or ROUTES_REGISTERED:
        return

    prompt_server = getattr(PromptServer, "instance", None)
    if prompt_server is None:
        return

    routes = prompt_server.routes

    @routes.options(API_BASE_PATH)
    async def oc_settings_presets_options(_request):
        return web.Response(status=204, headers=API_HEADERS)

    @routes.options(f"{API_BASE_PATH}/{{preset_name}}")
    async def oc_settings_preset_item_options(_request):
        return web.Response(status=204, headers=API_HEADERS)

    @routes.get(API_BASE_PATH)
    async def oc_settings_presets_list(_request):
        return json_response({
            "presets": PRESET_STORE.list_presets(),
            "directory": str(PRESET_STORE.ensure_dir()),
        })

    @routes.get(f"{API_BASE_PATH}/{{preset_name}}")
    async def oc_settings_presets_get(request):
        preset_name = request.match_info.get("preset_name", "")

        try:
            settings = PRESET_STORE.load(preset_name)
        except FileNotFoundError:
            return json_response({"error": "Preset not found."}, status=404)
        except json.JSONDecodeError:
            return json_response({"error": "Preset file is not valid JSON."}, status=500)

        return json_response({
            "name": preset_name,
            "settings": settings,
        })

    @routes.post(API_BASE_PATH)
    async def oc_settings_presets_save(request):
        try:
            payload = await request.json()
        except Exception:
            return json_response({"error": "Request body must be valid JSON."}, status=400)

        preset_name = payload.get("name", "")
        settings = payload.get("settings")
        if not str(preset_name).strip():
            return json_response({"error": "Preset name is required."}, status=400)
        if not isinstance(settings, dict):
            return json_response({"error": "settings must be a JSON object."}, status=400)

        saved = PRESET_STORE.save(preset_name, settings)
        return json_response(saved, status=201)

    ROUTES_REGISTERED = True


register_routes()

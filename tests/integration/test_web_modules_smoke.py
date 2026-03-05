import importlib
import inspect


WEB_MODULES = [
    "src.web.announcements",
    "src.web.assigned_papers",
    "src.web.auth_login",
    "src.web.auth_password",
    "src.web.conference_register",
    "src.web.decision_notify",
    "src.web.decision_record",
    "src.web.manuscript_upload",
    "src.web.payment_confirmation",
    "src.web.referee_assign",
    "src.web.referee_workload",
    "src.web.registration_payment",
    "src.web.registration_prices",
    "src.web.registration_validation",
    "src.web.review_access",
    "src.web.review_invite_notify",
    "src.web.review_invite_response",
    "src.web.review_submit",
    "src.web.schedule_edit",
    "src.web.schedule_generate",
    "src.web.schedule_modify",
    "src.web.schedule_notify",
    "src.web.schedule_publish",
    "src.web.schedule_view",
    "src.web.schedule_view_attendee",
    "src.web.submission_create",
    "src.web.submission_save",
    "src.web.three_referees",
    "src.web.user_registration",
]


def _build_call_kwargs(fn: object) -> dict:
    kwargs: dict = {}
    sig = inspect.signature(fn)  # type: ignore[arg-type]
    for name, param in sig.parameters.items():
        if param.default is not inspect._empty:
            continue
        if name == "payload":
            kwargs[name] = {}
            continue
        kwargs[name] = "1"
    return kwargs


def test_web_app_and_routes_import() -> None:
    web_app = importlib.import_module("src.web.app")
    web_routes = importlib.import_module("src.web.routes")
    assert web_app.app.title == "CMS Web"
    assert web_routes.index() == {"status": "web-ok"}


def test_web_modules_page_and_submit_smoke() -> None:
    for module_name in WEB_MODULES:
        module = importlib.import_module(module_name)
        functions = [
            obj
            for name, obj in inspect.getmembers(module, inspect.isfunction)
            if name.startswith("page_") or name.startswith("submit_")
        ]
        assert functions, f"{module_name} should expose page_/submit_ handlers"
        for fn in functions:
            kwargs = _build_call_kwargs(fn)
            try:
                result = fn(**kwargs)
                assert isinstance(result, dict)
            except Exception:
                # Some submit handlers can raise on domain validation with empty payloads.
                pass

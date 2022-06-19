# Объект для отрисовки шаблонов с помощью Jinja2Templates
from typing import Any

from starlette.requests import Request
from starlette.templating import Jinja2Templates

templates = Jinja2Templates(directory="website/templates")


def flash(request: Request, message: Any, category: str = "primary") -> None:
    """Функция, которая вставляет новую информацию в запрос для отрисовки уведомлений"""
    if "_messages" not in request.session:
        request.session["_messages"] = []
    request.session["_messages"].append({"message": message, "category": category})


def get_flashed_messages(request: Request):
    """Получение данных с запроса"""
    return request.session.pop("_messages") if "_messages" in request.session else []


# Регистрация функции внутри шаблонов
templates.env.globals["get_flashed_messages"] = get_flashed_messages

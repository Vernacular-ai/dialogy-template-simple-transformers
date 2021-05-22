import traceback
from datetime import datetime
from typing import Any, Dict, List

from dialogy.preprocess.text.normalize_utterance import normalize
from flask import jsonify, request

from slu import constants as const
from slu.src.api import app
from slu.src.controller.prediction import predict_wrapper
from slu.utils.config import Config
from slu.utils.sentry import capture_exception
from slu.utils import errors


PREDICT_API = predict_wrapper()
CONFIG = Config()


@app.route("/", methods=["GET"])
def health_check():
    """
    Get server status health.

    The purpose of this API is to help other people/machines know liveness of the application.
    """
    return jsonify(
        status="ok",
        response={"message": "Server is up."},
    )


@app.route("/predict/<lang>/<project_name>/", methods=["POST"])
def slu(lang: str, project_name: str):
    """
    Get SLU predictions.

    Produces a json response containing intents and entities.
    """
    supported_languages = list(CONFIG.get_supported_langauges().keys())
    if lang not in supported_languages:
        return errors.invalid_language(supported_languages)

    if not isinstance(request.json, dict):
        return errors.invalid_request(request.json)

    if not (const.ALTERNATIVES in request.json or const.TEXT in request.json):
        return errors.invalid_input(request.json)

    try:
        maybe_utterance: Any = request.json.get(const.ALTERNATIVES) or request.json.get(
            const.TEXT
        )

        sentences: List[str] = normalize(maybe_utterance)
        context: str = request.json.get(const.CONTEXT) or {}
        intents_info: List[Dict[str, Any]] = (
            request.json.get(const.S_INTENTS_INFO) or []
        )

        response = PREDICT_API(
            sentences,
            context,
            intents_info=intents_info,
            reference_time=int(datetime.now().timestamp() * 1000),
        )

        return jsonify(status="ok", response=response), 200

    except Exception as exc:
        # Update this section to:
        # 1. Handle specific errors
        # 2. provide user-friendly messages. The current is developer friendly.
        capture_exception(exc, ctx="api", message=request.json)
        return jsonify({"message": str(exc), "cause": traceback.format_exc()}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0")

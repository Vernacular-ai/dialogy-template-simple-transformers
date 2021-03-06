"""
Unit tests for predict function.

Test scenarios explicitly. The utility of the tests here are:

1. Introducing someone to this project should be a 
    breeze because they understand expectations, caveats, tricky cases here.

2. Improving components doesn't break an existing feature, because there is a test
    here to know about that.

3. The exceptions on sentry are minimal to none.

The tests here are not solid, they are just starting points.
"""
import os
import pathlib
import pytest
import json

from slu.src.controller.prediction import predict_wrapper
from slu import constants as const


predict = predict_wrapper()


def load_data():
    current_dir = pathlib.Path().absolute()
    base_path = os.path.join(current_dir)
    test_cases_path = os.path.join(base_path, "data", "test_cases.json")
    with open(test_cases_path, "r") as handle:
        test_cases = json.load(handle)
        # make any suitable modifications here
    return test_cases


@pytest.mark.parametrize("req", load_data())
def test_example(req):
    alternatives        = req.get(const.ALTERNATIVES, req[const.TEXT])
    context             = req.get(const.CONTEXT)
    intents_info        = req.get(const.S_INTENTS_INFO)
    expected_intent     = req["expected"][const.INTENT]
    expected_slot_value = req["expected"]["slot_value"]
    response            = predict(alternatives, context, intents_info=intents_info)

    assert response[const.INTENTS][0][const.NAME] == expected_intent

    if expected_slot_value:
        predicted_slot_value = response[const.INTENTS][0][const.SLOTS][0][const.VALUES][0][const.VALUE]
    else:
        predicted_slot_value = response[const.INTENTS][0][const.SLOTS]

    assert predicted_slot_value == expected_slot_value

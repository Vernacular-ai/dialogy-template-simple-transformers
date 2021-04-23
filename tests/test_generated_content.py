"""
test for generating a project and checking it's contents.

refer here:
https://github.com/copier-org/copier/blob/master/tests/test_complex_questions.py

"""
import sys
import os
import importlib

import pytest
import copier

def test_all_expected_generations():

    name_of_temp_dir = "temp_exp"
    name_of_gen_project = "hype"

    copier.copy(
        src_path="./",
        dst_path=f"./{name_of_temp_dir}/",
        data={
            "project_name": name_of_gen_project,
            "author_fullname": "testing_cow",
            "author_email": "testing_cow@vernacular.ai",
            "author_username": "testCow",
            "intent_classification_flavor": 1,
            "use_duckling": "yes",
            "use_ner": True
        },
        force=True
    )


    test_root = os.path.join(os.getcwd())
    sys.path.append(test_root)
    project_root = os.path.join(os.getcwd(), name_of_temp_dir)
    sys.path.append(project_root)

    train_py_present = os.path.exists(f"{name_of_temp_dir}/{name_of_gen_project}/dev/train.py")
    assert train_py_present == True

    evaluate_py_present = os.path.exists(f"{name_of_temp_dir}/{name_of_gen_project}/dev/evaluate.py")
    assert evaluate_py_present == True

    m = importlib.import_module(f"{name_of_temp_dir}.{name_of_gen_project}.dev.train")
    print(m)
    assert getattr(m, "train_ner_model") is not None
    assert getattr(m, "train_ner_model") is not None








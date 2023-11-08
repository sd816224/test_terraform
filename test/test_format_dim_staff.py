from src.transformation_lambda.transformation_lambda import format_dim_staff
import logging


def test_should_return_one_formatted_staff_member():
    input = {
        "staff": [
            {
                "staff_id": 1,
                "first_name": "Jeremie",
                "last_name": "Franey",
                "department_id": 2,
                "email_address": "jeremie.franey@terrifictotes.com",
                "created_at": "2022-11-03T14:20:51.563",
                "last_updated": "2022-11-03T14:20:51.563",
            }
        ],
        "department": [
            {
                "department_id": 1,
                "department_name": "Sales",
                "location": "Manchester",
                "manager": "Richard Roma",
                "created_at": "2022-11-03T14:20:49.962",
                "last_updated": "2022-11-03T14:20:49.962",
            },
            {
                "department_id": 2,
                "department_name": "Purchasing",
                "location": "Manchester",
                "manager": "Naomi Lapaglia",
                "created_at": "2022-11-03T14:20:49.962",
                "last_updated": "2022-11-03T14:20:49.962",
            },
        ],
    }
    expected = [
        [
            1,
            "Jeremie",
            "Franey",
            "Purchasing",
            "Manchester",
            "jeremie.franey@terrifictotes.com",
        ]
    ]
    actual = format_dim_staff(input)
    assert actual == expected


def test_should_return_two_formatted_staff_members():
    input = {
        "staff": [
            {
                "staff_id": 1,
                "first_name": "Jeremie",
                "last_name": "Franey",
                "department_id": 2,
                "email_address": "jeremie.franey@terrifictotes.com",
                "created_at": "2022-11-03T14:20:51.563",
                "last_updated": "2022-11-03T14:20:51.563",
            },
            {
                "staff_id": 4,
                "first_name": "Ana",
                "last_name": "Glover",
                "department_id": 3,
                "email_address": "ana.glover@terrifictotes.com",
                "created_at": "2022-11-03T14:20:51.563",
                "last_updated": "2022-11-03T14:20:51.563",
            },
        ],
        "department": [
            {
                "department_id": 2,
                "department_name": "Purchasing",
                "location": "Manchester",
                "manager": "Naomi Lapaglia",
                "created_at": "2022-11-03T14:20:49.962",
                "last_updated": "2022-11-03T14:20:49.962",
            },
            {
                "department_id": 3,
                "department_name": "Dispatch",
                "location": "Leds",
                "manager": "Mark Hanna",
                "created_at": "2022-11-03T14:20:49.962",
                "last_updated": "2022-11-03T14:20:49.962",
            },
        ],
    }
    expected = [
        [
            1,
            "Jeremie",
            "Franey",
            "Purchasing",
            "Manchester",
            "jeremie.franey@terrifictotes.com",
        ],
        [
            4,
            "Ana",
            "Glover",
            "Dispatch",
            "Leds",
            "ana.glover@terrifictotes.com",
        ],  # noqa E501,
    ]

    actual = format_dim_staff(input)
    assert actual == expected


def test_should_return_only_correctly_formatted_staff(caplog):
    with caplog.at_level(logging.INFO):
        input = {
            "staff": [
                {
                    "staff_id": 1,
                    "first_name": "Jeremie",
                    "last_name": "Franey",
                    "department_id": 2,
                    "email_address": "jeremie.franey@terrifictotes.com",
                    "created_at": "2022-11-03T14:20:51.563",
                    "last_updated": "2022-11-03T14:20:51.563",
                },
                {
                    "staff_id": 4,
                    "first_name": "Ana",
                    "last_name": "Glover",
                    "department_id": 3,
                    "email_address": "ana.glover@terrifictotes.com",
                    "created_at": "2022-11-03T14:20:51.563",
                    "last_updated": "2022-11-03T14:20:51.563",
                },
            ],
            "department": [
                {
                    "department_id": 2,
                    "department_name": "Purchasing",
                    "location": "Manchester",
                    "manager": "Naomi Lapaglia",
                    "created_at": "2022-11-03T14:20:49.962",
                    "last_updated": "2022-11-03T14:20:49.962",
                },
                {
                    "department_id": 4,
                    "department_name": "Dispatch",
                    "location": "Leds",
                    "manager": "Mark Hanna",
                    "created_at": "2022-11-03T14:20:49.962",
                    "last_updated": "2022-11-03T14:20:49.962",
                },
            ],
        }
        expected = [
            [
                1,
                "Jeremie",
                "Franey",
                "Purchasing",
                "Manchester",
                "jeremie.franey@terrifictotes.com",
            ]
        ]

        actual = format_dim_staff(input)
        assert actual == expected
        assert "staff_id 4: no valid department_id" in caplog.text


def test_KeyError_when_incorrect_data_passed(caplog):
    with caplog.at_level(logging.ERROR):
        input = {
            "design": [
                {
                    "design_id": 8,
                    "created_at": "2022-11-03T14:20:49.962",
                    "design_name": "Wooden",
                    "file_location": "/usr",
                    "file_name": "wooden-20220717-npgz.json",
                    "last_updated": "2022-11-03T14:20:49.962",
                }
            ]
        }
        format_dim_staff(input)
        assert "Incorrect staff data provided" in caplog.text


def test_AttributeError_when_incorrect_data_type_passed(caplog):
    with caplog.at_level(logging.ERROR):
        input = "hello"
        format_dim_staff(input)
        assert "'str' object has no attribute 'keys'" in caplog.text

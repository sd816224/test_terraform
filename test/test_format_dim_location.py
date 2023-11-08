from src.transformation_lambda.transformation_lambda import format_dim_location
import logging

logger = logging.getLogger("TestLogger")
logger.setLevel(logging.INFO)


def test_extract_correct_values():
    """
    This tests that format_dim_location extracts the values from all columns
    in the address table except for created_at and last_updated.
    """
    json = {
        "address": [
            {
                "address_id": 1,
                "address_line_1": "6826 Herzog Via",
                "address_line_2": None,
                "district": "Avon",
                "city": "New Patienceburgh",
                "postal_code": "28441",
                "country": "Turkey",
                "phone": "1803 637401",
                "created_at": "2022-11-03T14:20:49.962",
                "last_updated": "2022-11-03T14:20:49.962",
            }
        ]
    }
    expected = [
        [
            1,
            "6826 Herzog Via",
            None,
            "Avon",
            "New Patienceburgh",
            "28441",
            "Turkey",
            "1803 637401",
        ]
    ]

    assert format_dim_location(json) == expected


def test_works_for_multiple_dicts():
    json = {
        "address": [
            {
                "address_id": 1,
                "address_line_1": "6826 Herzog Via",
                "address_line_2": None,
                "district": "Avon",
                "city": "New Patienceburgh",
                "postal_code": "28441",
                "country": "Turkey",
                "phone": "1803 637401",
                "created_at": "2022-11-03T14:20:49.962",
                "last_updated": "2022-11-03T14:20:49.962",
            },
            {
                "address_id": 2,
                "address_line_1": "179 Alexie Cliffs",
                "address_line_2": None,
                "district": None,
                "city": "Aliso Viejo",
                "postal_code": "99305-7380",
                "country": "San Marino",
                "phone": "9621 880720",
                "created_at": "2022-11-03T14:20:49.962",
                "last_updated": "2022-11-03T14:20:49.962",
            },
            {
                "address_id": 3,
                "address_line_1": "148 Sincere Fort",
                "address_line_2": None,
                "district": None,
                "city": "Lake Charles",
                "postal_code": "89360",
                "country": "Samoa",
                "phone": "0730 783349",
                "created_at": "2022-11-03T14:20:49.962",
                "last_updated": "2022-11-03T14:20:49.962",
            },
        ]
    }
    expected = [
        [
            1,
            "6826 Herzog Via",
            None,
            "Avon",
            "New Patienceburgh",
            "28441",
            "Turkey",
            "1803 637401",
        ],
        [
            2,
            "179 Alexie Cliffs",
            None,
            None,
            "Aliso Viejo",
            "99305-7380",
            "San Marino",
            "9621 880720",
        ],
        [
            3,
            "148 Sincere Fort",
            None,
            None,
            "Lake Charles",
            "89360",
            "Samoa",
            "0730 783349",
        ],
    ]
    assert format_dim_location(json) == expected


def test_ignores_duplicate_errors():
    json = {
        "address": [
            {
                "address_id": 1,
                "address_line_1": "6826 Herzog Via",
                "address_line_2": None,
                "district": "Avon",
                "city": "New Patienceburgh",
                "postal_code": "28441",
                "country": "Turkey",
                "phone": "1803 637401",
                "created_at": "2022-11-03T14:20:49.962",
                "last_updated": "2022-11-03T14:20:49.962",
            },
            {
                "address_id": 2,
                "address_line_1": "179 Alexie Cliffs",
                "address_line_2": None,
                "district": None,
                "city": "Aliso Viejo",
                "postal_code": "99305-7380",
                "country": "San Marino",
                "phone": "9621 880720",
                "created_at": "2022-11-03T14:20:49.962",
                "last_updated": "2022-11-03T14:20:49.962",
            },
            {
                "address_id": 3,
                "address_line_1": "148 Sincere Fort",
                "address_line_2": None,
                "district": None,
                "city": "Lake Charles",
                "postal_code": "89360",
                "country": "Samoa",
                "phone": "0730 783349",
                "created_at": "2022-11-03T14:20:49.962",
                "last_updated": "2022-11-03T14:20:49.962",
            },
            {
                "address_id": 3,
                "address_line_1": "148 Sincere Fort",
                "address_line_2": None,
                "district": None,
                "city": "Lake Charles",
                "postal_code": "89360",
                "country": "Samoa",
                "phone": "0730 783349",
                "created_at": "2022-11-03T14:20:49.962",
                "last_updated": "2022-11-03T14:20:49.962",
            },
        ]
    }
    expected = [
        [
            1,
            "6826 Herzog Via",
            None,
            "Avon",
            "New Patienceburgh",
            "28441",
            "Turkey",
            "1803 637401",
        ],
        [
            2,
            "179 Alexie Cliffs",
            None,
            None,
            "Aliso Viejo",
            "99305-7380",
            "San Marino",
            "9621 880720",
        ],
        [
            3,
            "148 Sincere Fort",
            None,
            None,
            "Lake Charles",
            "89360",
            "Samoa",
            "0730 783349",
        ],
    ]
    assert format_dim_location(json) == expected


def test_does_not_mutate_json_data():
    json = {
        "address": [
            {
                "address_id": 1,
                "address_line_1": "6826 Herzog Via",
                "address_line_2": None,
                "district": "Avon",
                "city": "New Patienceburgh",
                "postal_code": "28441",
                "country": "Turkey",
                "phone": "1803 637401",
                "created_at": "2022-11-03T14:20:49.962",
                "last_updated": "2022-11-03T14:20:49.962",
            },
            {
                "address_id": 2,
                "address_line_1": "179 Alexie Cliffs",
                "address_line_2": None,
                "district": None,
                "city": "Aliso Viejo",
                "postal_code": "99305-7380",
                "country": "San Marino",
                "phone": "9621 880720",
                "created_at": "2022-11-03T14:20:49.962",
                "last_updated": "2022-11-03T14:20:49.962",
            },
            {
                "address_id": 3,
                "address_line_1": "148 Sincere Fort",
                "address_line_2": None,
                "district": None,
                "city": "Lake Charles",
                "postal_code": "89360",
                "country": "Samoa",
                "phone": "0730 783349",
                "created_at": "2022-11-03T14:20:49.962",
                "last_updated": "2022-11-03T14:20:49.962",
            },
            {
                "address_id": 3,
                "address_line_1": "148 Sincere Fort",
                "address_line_2": None,
                "district": None,
                "city": "Lake Charles",
                "postal_code": "89360",
                "country": "Samoa",
                "phone": "0730 783349",
                "created_at": "2022-11-03T14:20:49.962",
                "last_updated": "2022-11-03T14:20:49.962",
            },
        ]
    }
    expected = {
        "address": [
            {
                "address_id": 1,
                "address_line_1": "6826 Herzog Via",
                "address_line_2": None,
                "district": "Avon",
                "city": "New Patienceburgh",
                "postal_code": "28441",
                "country": "Turkey",
                "phone": "1803 637401",
                "created_at": "2022-11-03T14:20:49.962",
                "last_updated": "2022-11-03T14:20:49.962",
            },
            {
                "address_id": 2,
                "address_line_1": "179 Alexie Cliffs",
                "address_line_2": None,
                "district": None,
                "city": "Aliso Viejo",
                "postal_code": "99305-7380",
                "country": "San Marino",
                "phone": "9621 880720",
                "created_at": "2022-11-03T14:20:49.962",
                "last_updated": "2022-11-03T14:20:49.962",
            },
            {
                "address_id": 3,
                "address_line_1": "148 Sincere Fort",
                "address_line_2": None,
                "district": None,
                "city": "Lake Charles",
                "postal_code": "89360",
                "country": "Samoa",
                "phone": "0730 783349",
                "created_at": "2022-11-03T14:20:49.962",
                "last_updated": "2022-11-03T14:20:49.962",
            },
            {
                "address_id": 3,
                "address_line_1": "148 Sincere Fort",
                "address_line_2": None,
                "district": None,
                "city": "Lake Charles",
                "postal_code": "89360",
                "country": "Samoa",
                "phone": "0730 783349",
                "created_at": "2022-11-03T14:20:49.962",
                "last_updated": "2022-11-03T14:20:49.962",
            },
        ]
    }
    format_dim_location(json)
    assert json == expected


def test_should_log_a_warning_if_key_is_missing(caplog):
    with caplog.at_level(logging.ERROR):
        json = {"sales_order": [{"spam": "eggs"}]}
        format_dim_location(json)
        assert "KeyError: missing key 'address'." in caplog.text
        json = {"address": [{"spam": "eggs"}]}
        format_dim_location(json)
        assert "KeyError: missing key 'address_id'." in caplog.text

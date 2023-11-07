from src.transformation_lambda.format_dim_counterparty import format_dim_counterparty # noqa E501
import pytest
import logging

test_table = {
            "address": [{
                "address_id": 1,
                "address_line_1": "6826 Herzog Via",
                "address_line_2": None,
                "district": "Avon", "city":
                "New Patienceburgh",
                "postal_code": "28441",
                "country": "Turkey",
                "phone": "1803 637401",
                "created_at": "2022-11-03T14:20:49.962",
                "last_updated": "2022-11-03T14:20:49.962"
            }, {
                "address_id": 2,
                "address_line_1": "179 Alexie Cliffs",
                "address_line_2": None,
                "district": None,
                "city": "Aliso Viejo",
                "postal_code": "99305-7380",
                "country": "San Marino",
                "phone": "9621 880720",
                "created_at": "2022-11-03T14:20:49.962",
                "last_updated": "2022-11-03T14:20:49.962"
            }
            ],

            "counterparty": [{
                "counterparty_id": 1,
                "counterparty_legal_name": "Fahey and Sons",
                "legal_address_id": 1,
                "commercial_contact": "Micheal Toy",
                "delivery_contact": "Mrs. Lucy Runolfsdottir",
                "created_at": "2022-11-03T14:20:51.563",
                "last_updated": "2022-11-03T14:20:51.563"
                }]
}


def test_output_rows_has_correct_key_names():
    result = format_dim_counterparty(test_table)
    for row in result:
        assert 'counterparty_id' in row
        assert 'counterparty_legal_name' in row
        assert 'counterparty_legal_address_line_1' in row
        assert 'counterparty_legal_address_line_2' in row
        assert 'counterparty_legal_district' in row
        assert 'counterparty_legal_city' in row
        assert 'counterparty_legal_postal_code' in row
        assert 'counterparty_legal_country' in row
        assert 'counterparty_legal_phone_number' in row
        assert len(row) == 9


def test_correct_output():
    result = format_dim_counterparty(test_table)
    assert len(result) == 1
    assert {'counterparty_id': 1,
            'counterparty_legal_name': "Fahey and Sons",
            'counterparty_legal_address_line_1': "6826 Herzog Via",
            'counterparty_legal_address_line_2': None,
            'counterparty_legal_district': "Avon",
            'counterparty_legal_city': "New Patienceburgh",
            'counterparty_legal_postal_code': "28441",
            'counterparty_legal_country': "Turkey",
            'counterparty_legal_phone_number': "1803 637401", } in result


def test_KeyError_happend_when_wrong_table_name(caplog):
    wrong_table = {'staff': test_table['counterparty']}
    with caplog.at_level(logging.ERROR):
        format_dim_counterparty(wrong_table)
        assert 'Error retrieving data' in caplog.text


def test_RuntimeError_happend_when_wrong_input():
    with pytest.raises(RuntimeError):
        format_dim_counterparty(5)

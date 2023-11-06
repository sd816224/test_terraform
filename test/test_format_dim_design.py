from src.transformation_lambda.format_dim_design import format_dim_design
import pytest
import logging

test_table = {
    "design": [
        {
            "design_id": 1,
            "created_at": "2023-10-30T08:27:09.957",
            "last_updated": "2023-10-30T08:27:09.957",
            "design_name": 'leee-design',
            "file_location": '/hello/here',
            "file_name": 'test_file.jpg',
        },
        {
            "design_id": 2,
            "created_at": "2023-11-30T08:27:09.957",
            "last_updated": "2023-12-30T08:27:09.957",
            "design_name": 'sam-design',
            "file_location": '/hello/here/sam',
            "file_name": 'test_file2.jpg',
        },
        {
            "design_id": 3,
            "created_at": "2023-05-30T08:27:09.957",
            "last_updated": "2023-06-30T08:27:09.957",
            "design_name": 'yoman-design',
            "file_location": '/hello/here/yoman',
            "file_name": 'test_file3.jpg',
        }
    ]
}


def test_output_rows_has_correct_key_names():
    result = format_dim_design(test_table)
    for row in result:
        assert 'design_id' in row
        assert 'design_name' in row
        assert 'file_location' in row
        assert 'file_name' in row
        assert len(row) == 4


def test_correct_output():
    result = format_dim_design(test_table)
    assert len(result) == 3
    assert {'design_id': 1,
            'design_name': 'leee-design',
            'file_location': '/hello/here',
            'file_name': 'test_file.jpg'} in result

    assert {'design_id': 2,
            'design_name': 'sam-design',
            'file_location': '/hello/here/sam',
            'file_name': 'test_file2.jpg'} in result
    assert {'design_id': 3,
            'design_name': 'yoman-design',
            'file_location': '/hello/here/yoman',
            'file_name': 'test_file3.jpg'} in result


def test_KeyError_happend_when_wrong_table_name(caplog):
    wrong_table = {'staff': test_table['design']}
    with caplog.at_level(logging.ERROR):
        format_dim_design(wrong_table)
        assert 'Error retrieving data' in caplog.text


def test_RuntimeError_happend_when_wrong_input():
    with pytest.raises(RuntimeError):
        format_dim_design(5)

from src.transformation_lambda.format_dim_date import format_dim_date
import json

def test_get_json():
    f=open('test/test_OLTP_sale_orders_content.json')
    table=json.load(f)
    format_dim_date(table)
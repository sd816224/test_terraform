from src.loading_lambda.regex_util import escape_apostrophe

def test_test():
    assert escape_apostrophe("O'Brien") == "O''Brien"

    
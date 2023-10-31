# Running the Makefile

# 1 In the terminal, navigate to the root directory of the project and run:
    make requirements

# 2 Then run:
    make run-checks

# Do not commit or deploy if:
    Coverage is less than 90%,
    flake8 fails,
    if any unit-tests fail.

# PSA, to add requirements to the requirements.txt file run:
    make add-requirements
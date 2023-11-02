def lambda_handler(event, context):
    credentials = get_credentials("totesys-production")

    connection = get_connetion(credentials)

    data = get_data(connection)

    get_last_upload("")

    write_file

    pass

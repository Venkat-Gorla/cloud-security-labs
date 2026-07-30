def get_table_names(client) -> set[str]:
    """
    Return the names of all DynamoDB tables in the account.
    """
    paginator = client.get_paginator("list_tables")
    table_names: set[str] = set()

    for page in paginator.paginate():
        table_names.update(page["TableNames"])

    return table_names

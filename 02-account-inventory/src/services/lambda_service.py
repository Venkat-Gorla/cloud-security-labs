def get_function_names(lambda_client) -> set[str]:
    """
    Return the names of all Lambda functions in the account.
    """
    paginator = lambda_client.get_paginator("list_functions")
    function_names: set[str] = set()

    for page in paginator.paginate():
        for function in page["Functions"]:
            function_names.add(function["FunctionName"])

    return function_names


def get_unmanaged_functions(
    lambda_client,
    managed_functions: set[str],
) -> list[str]:
    """
    Return Lambda functions not managed by CloudFormation.
    """
    function_names = get_function_names(lambda_client)
    unmanaged = function_names - managed_functions

    return sorted(unmanaged)

import inspect

def recreate_function(original_function, additional_behaviour):
    """
    :param function original_function
    :param function additional_behaviour
    Because pytest needs to look at the function arguments in order to inject
    the fixtures, we'll need to recreate functions exactly as they were passed
    """
    local_vars = {}
    global_vars = {"additional_behaviour":additional_behaviour}
    original_function_signature = inspect.signature(original_function)
    additional_behaviour_signature_list = list(inspect.signature(additional_behaviour).parameters)
    try:
        additional_behaviour_signature_list.remove("function_args")
    except:
        pass

    new_function_signature = "("
    additional_behaviour_signature = "("
    for param_name in additional_behaviour_signature_list:
        new_function_signature += param_name+","
        additional_behaviour_signature += param_name+","
    if original_function_signature.parameters:
        additional_behaviour_signature += "function_args=["
    for param_name in original_function_signature.parameters:
        new_function_signature += param_name+","
        additional_behaviour_signature += param_name+","
    new_function_signature = new_function_signature[0:-1]+")"
    additional_behaviour_signature = additional_behaviour_signature[0:-1]
    if original_function_signature.parameters:
        additional_behaviour_signature += "])"
    else:
        additional_behaviour_signature += ")"

    print("new_function_signature", new_function_signature)
    print("additional_behaviour_signature", additional_behaviour_signature)
    func_string = "def new_func{0}:\n  return additional_behaviour{1}".format(new_function_signature, additional_behaviour_signature)
    exec(func_string, global_vars, local_vars)
    return local_vars["new_func"]


if __name__ == "__main__":

    def some_func(alpha, beta, gamma):
        pass

    def additional_func(function_args):
        print("function_args", function_args)
        assert len(function_args) == 3

    new_func = recreate_function(some_func, additional_func)
    new_signature = inspect.signature(some_func)
    assert new_signature.parameters["alpha"]
    assert new_signature.parameters["beta"]
    assert new_signature.parameters["gamma"]
    new_func(1,2,3)

    def additional_func2(test_fixture, function_args):
        print("test_fixture", test_fixture)
        assert test_fixture == "test"
        print("function_args", function_args)
        assert len(function_args) == 3

    new_func = recreate_function(some_func, additional_func2)
    new_signature = inspect.signature(some_func)
    assert new_signature.parameters["alpha"]
    assert new_signature.parameters["beta"]
    assert new_signature.parameters["gamma"]
    new_func("test",1,2,3)

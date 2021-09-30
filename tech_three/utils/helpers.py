

def exception_handler(exc, context):
    from rest_framework.views import exception_handler
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    resp = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if resp is not None:
        if isinstance(resp.data, dict):
            data = dict()
            for key, value in resp.data.items():
                if isinstance(value, list):
                    # Serializers
                    if isinstance(value[0], dict):
                        for _key, _value in value[0].items():
                            data.update({_key: _value})

                    elif isinstance(value[0], list) or value[0].code == 'list':
                        # If errors needs to be listed as list
                        data.update({key: value})

                    elif isinstance(value[0], str):
                        data.update({key: ', '.join(value)})

                elif isinstance(value, dict):
                    # Child Serializers
                    for _key, _value in value.items():
                        if isinstance(_value, list):
                            try:
                                data.update({_key: ', '.join(_value)})
                            except TypeError:
                                for __value in _value:
                                    if isinstance(__value, dict):
                                        for ___key, ___value in __value.items():
                                            data.update({___key: ', '.join(___value)})

                        elif isinstance(_value, dict):
                            # Grand Child Serializers
                            for __key, __value in _value.items():
                                if isinstance(__value, list):
                                    data.update({__key: ', '.join(__value)})
                                elif isinstance(__value, dict):
                                    # Super Grand Child Serializers
                                    for ___key, ___value in __value.items():
                                        data.update({___key: ', '.join(___value)})

        else:
            data = list()
            for value in resp.data:
                for key, val in value.items():
                    data.append({key: ', '.join(val)})

        resp.data = data

        # resp.data['status_code'] = resp.status_code

    return resp

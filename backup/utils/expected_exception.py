EXPECTED_EXCEPTION_ATTR = 'is_expected'

def expected_exception(exception: BaseException) -> BaseException:
    setattr(exception, EXPECTED_EXCEPTION_ATTR, True)
    return exception
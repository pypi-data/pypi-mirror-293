class CometException(Exception):
    pass


class DatasetItemUpdateOperationRequiresItemId(CometException):
    pass


class ContextExtractorNotSet(CometException):
    pass

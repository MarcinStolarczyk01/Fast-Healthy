class IncompleteProductInfoError(Exception):
    def __init__(
        self,
        message="Missing macro or unit information for product named. \
                                Complete product attributes in a database.",
    ):
        self.message = message
        super().__init__(self.message)

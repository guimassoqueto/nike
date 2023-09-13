class APIHasChangedError(Exception):
    def __init__(self, *args):
        super().__init__(args)

    def __str__(self):
        return f'Nike offers API has changed. Please update the variable NIKE_OFFERS_API in app/settings.py'
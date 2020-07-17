class Item:
    def __init__(self, use_function=None, targeting=False, missile=False, targeting_message=None, **kwargs):
        pass
        self.use_function = use_function
        self.targeting = targeting
        self.missile = missile
        self.targeting_message = targeting_message
        self.function_kwargs = kwargs
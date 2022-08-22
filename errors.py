class AppError(Exception):
    def __init__(self, err=None):
        if err:
            self.message = err
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return f'AppError: {self.message}'
        else:
            return f'AppError raised, description failed'

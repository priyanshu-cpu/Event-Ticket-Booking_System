class EmailAlreadyExists(Exception):
    def __init__(self, email:str):
        self.email = email
        super().__init__(f"Email already registered: {email}")


class InvalidCredentials(Exception):
    def __init__(self):
        super().__init__("Invalid credentials")



class NotFound(Exception):
    pass
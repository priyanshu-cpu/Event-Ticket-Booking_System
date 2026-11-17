class EmailAlreadyExists(Exception):
    def __init__(self, email:str):
        self.email = email
        super().__init__(f"Email already registered: {email}")


class InvalidCredentials(Exception):
    def __init__(self):
        super().__init__("Invalid credentials")



class NotFound(Exception):
    pass


class AlreadyExists(Exception):
    pass

class Unauthorized(Exception):
    pass


class DoesntExist(Exception):
    pass

class EventNotFound(Exception):
    pass

class SeatNotFound(Exception):
    pass

class SeatDoesNotBelong(Exception):
    pass

class SeatHeldOrBooked(Exception):
    pass

class SeatHeld(Exception):
    pass

class CanNotConfirm(Exception):
    pass
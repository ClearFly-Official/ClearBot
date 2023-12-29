from discord.ext import commands


class MissingPermissions(commands.CommandError):
    def __init__(self):
        super().__init__(f"User is not authorised.")


class VAError(commands.CommandError):
    def __init__(self):
        super().__init__()


class UserVABanned(VAError):
    def __init__(self):
        super().__init__()


class UserNotVA(VAError):
    def __init__(self):
        super().__init__()

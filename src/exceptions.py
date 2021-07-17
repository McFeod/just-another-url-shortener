class IncorrectDBUsage(Exception):
    pass


class LinkCollision(IncorrectDBUsage):
    pass


class LinkNotFound(IncorrectDBUsage):
    pass
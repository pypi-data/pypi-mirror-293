class Ticket:
    id: str
    quantity: str
    type: int # 1 = default (price), 2 = (accessoirs like bikes)

    def __init__(self, id, quantity, ticket_type=1):
        self.id = id
        self.quantity = quantity
        self.type = ticket_type

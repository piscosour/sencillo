class User:

	"""A registered user with an account."""

	def __init__(self, username, password, email, phone=None):
		self.username = username
		self.password = password
		self.email = email
		self.phone = phone


class Payment:

	"""A transaction made through the system."""

	def __init__(self, sender, recipient, amount, timestamp, description=None):
		self.sender = sender
		self.recipient = recipient
		self.amount = amount
		self.timestamp = timestamp
		self.description = description


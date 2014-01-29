class User:

	"""A registered user with an account."""

	def __init__(self, username, email, credit, mobile=None):
		self.username = username
		self.email = email
		self.credit = credit
		self.mobile = mobile



class Payment:

	"""A transaction made through the system."""

	def __init__(self, sender, recipient, amount, timestamp, description=None):
		self.sender = sender
		self.recipient = recipient
		self.amount = amount
		self.timestamp = timestamp
		self.description = description


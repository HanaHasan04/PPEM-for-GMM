class Server:
  """
  This class represents the server - an untrusted third party.

  Attributes:
  -----------
  num_of_clients:
      The total number of clients (data points).

  vectors:
      The encrypted vectors sent by clients.
  """

  def __init__(self, num_of_clients):
    self.num_of_clients = num_of_clients
    self.vectors = []

  def add_vec(self, vector):
    """Adds an encrypted vector to the server's list of encrypted vectors."""
    self.vectors.append(vector)

  def calc_sum(self):
    """Calculates the sum of the encrypted vectors stored on the server."""
    if len(self.vectors) != self.num_of_clients:
      raise ValueError("The number of vectors stored on the server does not match the number of clients.")
    return sum(self.vectors)

  def clear_server(self):
    """Clears the server's list of encrypted vectors."""
    self.vectors = []

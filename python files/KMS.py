import tenseal as ts


class KMS:
  """
  This class represents a Key Management Service (KMS).
  Our KMS is used to generate, distribute, and manage cryptographic keys for the CKKS scheme via TenSEAL library.

  Attributes:
  -----------
  poly_modulus_degree:
      The degree of the polynomial modulus used in the CKKS scheme.

  coeff_mod_bit_sizes:
      The bit sizes of the coefficient modulus used in the CKKS scheme.

  context: TenSEALContext
      The parameters of the CKKS scheme in TenSEAL.

  clients:
      The list of clients (parties).
  """
  
  def __init__(self, clients, poly_modulus_degree = 8192, coeff_mod_bit_sizes = [60, 40, 40, 60], global_scale = 2 ** 40):
    self.poly_modulus_degree = poly_modulus_degree
    self.coeff_mod_bit_sizes = coeff_mod_bit_sizes
    self.global_scale = global_scale
    self.context = None
    self.clients = clients

  def gen_context(self):
    """Generates a TenSEALContext."""
    self.context = ts.context(ts.SCHEME_TYPE.CKKS, poly_modulus_degree=self.poly_modulus_degree, coeff_mod_bit_sizes=self.coeff_mod_bit_sizes)
    self.context.generate_galois_keys()
    self.context.global_scale = self.global_scale

  def dist_context(self):
    """Distributes the current context to the list of clients."""
    for client in self.clients:
      client.context = self.context

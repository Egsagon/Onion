# ==================== #
# === Onion Errors === #
# ==================== #

class E(BaseException): pass # Base error

class SizeErr(E): pass

class OriginErr(E): pass

class PixErr(E): pass
import uuid

def generate_sku(prefix='SKU', length=8):
    return f"{prefix}-{uuid.uuid4().hex[:length].upper()}"
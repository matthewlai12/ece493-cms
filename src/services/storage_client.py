def store_file(storage_key: str, payload: bytes) -> dict:
    return {"storage_key": storage_key, "size_bytes": len(payload)}

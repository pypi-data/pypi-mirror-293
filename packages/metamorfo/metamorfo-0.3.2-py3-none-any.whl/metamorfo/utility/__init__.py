import hashlib
import base64


def hexa_b64(data: str):
    """
    Codifica uma string para base64 e retorna o valor.
    """
    encoded_bytes = base64.b64encode(data.encode("utf-8"))
    return encoded_bytes.decode("utf-8")


def decode_b64(encoded_data: str):
    """
    Recebe uma string codificada em base64 e retorna o valor decodificado.
    """
    decoded_bytes = base64.b64decode(encoded_data)
    return decoded_bytes.decode("utf-8")


def hexa_md5(data: str):
    """
    Codifica uma string para md5 e retorna o valor.
    """
    response = hashlib.md5(data.encode()).hexdigest()
    return response


def hexa_sha256(data: str):
    """
    Codifica uma string para sha256 e retorna o valor.
    """
    response = hashlib.sha256(data.encode()).digest()
    return response.hex()


def list_in_query(
    lista: list, nome_parametro: str, query: str, parametros: dict
):
    """
    Adiciona uma lista de parâmetros à query.
    """
    listaitems = [f":{nome_parametro}_{i}" for i, _ in enumerate(lista)]
    query = query.replace(f":{nome_parametro}", ",".join(listaitems))
    for i, x in enumerate(listaitems):
        parametros[x.replace(":", "")] = lista[i]

    return query, parametros

def success_response(data: dict = None, message: str = None, status: int = 200):
    """
    Retorna uma resposta padrão de sucesso.
    """
    response = {"status": "success"}

    if message:
        response["message"] = message

    if data:
        response.update(data)

    return response, status


def error_response(message: str = "Ocorreu um erro", status: int = 400):
    """
    Retorna uma resposta padrão de erro.
    """
    return {
        "status": "error",
        "message": message
    }, status

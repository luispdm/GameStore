from django.http import JsonResponse


def json_400(error=None):
    if error is None:
        error="Bad request"
    d = {
        "error": error
    }
    return JsonResponse(status=400, data=d)


def json_405(error=None):
    if error is None:
        error="Method not supported"
    d = {
        "error": error
    }
    return JsonResponse(status=405, data=d)


def json_404(error=None):
    if error is None:
        error="Resource not found"
    d = {
        "error": error
    }
    return JsonResponse(status=404, data=d)
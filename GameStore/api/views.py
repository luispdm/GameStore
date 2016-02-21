from django.core.urlresolvers import reverse, resolve
from django.http import JsonResponse


# Simply shows available versions
def api(request):
    if request.method == "GET":
        return JsonResponse({
            'urls': {
                'v1':request.build_absolute_uri(reverse('v1')),
                'self': request.build_absolute_uri()
            }
        })
    else:
        # This view only supports GET
        return JsonResponse(status=405, data=None)
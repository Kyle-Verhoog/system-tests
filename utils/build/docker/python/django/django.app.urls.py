# pages/urls.py
from ddtrace import tracer
from django.http import HttpResponse
from django.urls import path
from django.http import JsonResponse
from iast import (
    weak_hash_secure_algorithm,
    weak_hash,
    weak_hash_multiple,
    weak_hash_duplicates,
    weak_cipher,
    weak_cipher_secure_algorithm,
)

import requests


try:
    from ddtrace.contrib.trace_utils import set_user
except ImportError:
    set_user = lambda *args, **kwargs: None

tracer.trace("init.service").finish()


def hello_world(request):
    return HttpResponse("Hello, World!")


def sample_rate(request, i):
    return HttpResponse("OK")


def waf(request, *args, **kwargs):
    return HttpResponse("Hello, World!")


def headers(request):
    response = HttpResponse("OK")
    response["Content-Language"] = "en-US"
    return response


def status_code(request, *args, **kwargs):
    return HttpResponse("OK, probably", status=int(request.GET.get("code", "200")))


def identify(request):
    set_user(
        tracer,
        user_id="usr.id",
        email="usr.email",
        name="usr.name",
        session_id="usr.session_id",
        role="usr.role",
        scope="usr.scope",
    )
    return HttpResponse("OK")


def identify_propagate(request):
    set_user(
        tracer,
        user_id="usr.id",
        email="usr.email",
        name="usr.name",
        session_id="usr.session_id",
        role="usr.role",
        scope="usr.scope",
        propagate=True,
    )
    return HttpResponse("OK")


def view_weak_hash_multiple_hash(request):
    weak_hash_multiple()
    return HttpResponse("OK")


def view_weak_hash_secure_algorithm(request):
    result = weak_hash_secure_algorithm()
    return HttpResponse("OK")


def view_weak_hash_md5_algorithm(request):
    result = weak_hash()
    return HttpResponse("OK")


def view_weak_hash_deduplicate(request):
    result = weak_hash_duplicates()
    return HttpResponse("OK")


def view_weak_cipher_insecure(request):
    weak_cipher()
    return HttpResponse("OK")


def view_weak_cipher_secure(request):
    weak_cipher_secure_algorithm()
    return HttpResponse("OK")


def make_distant_call(request):
    # curl localhost:7777/make_distant_call?url=http%3A%2F%2Fweblog%3A7777 | jq

    url = request.GET.get("url")
    response = requests.get(url)

    result = {
        "url": url,
        "status_code": response.status_code,
        "request_headers": dict(response.request.headers),
        "response_headers": dict(response.headers),
    }

    return JsonResponse(result)


urlpatterns = [
    path("", hello_world),
    path("sample_rate_route/<int:i>", sample_rate),
    path("waf", waf),
    path("waf/", waf),
    path("waf/<url>", waf),
    path("params/<appscan_fingerprint>", waf),
    path("headers", headers),
    path("status", status_code),
    path("identify", identify),
    path("identify-propagate", identify_propagate),
    path("iast/insecure_hashing/multiple_hash", view_weak_hash_multiple_hash),
    path("iast/insecure_hashing/test_secure_algorithm", view_weak_hash_secure_algorithm),
    path("iast/insecure_hashing/test_md5_algorithm", view_weak_hash_md5_algorithm),
    path("iast/insecure_hashing/deduplicate", view_weak_hash_deduplicate),
    path("iast/insecure_cipher/test_insecure_algorithm", view_weak_cipher_insecure),
    path("iast/insecure_cipher/test_secure_algorithm", view_weak_cipher_secure),
    path("make_distant_call", make_distant_call),
]

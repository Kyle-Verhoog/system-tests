from typing import Any

import pytest

from parametric.spec.trace import SAMPLING_PRIORITY_KEY, ORIGIN
from parametric.utils.headers import make_single_request_and_get_inject_headers
from parametric.utils.test_agent import get_span

parametrize = pytest.mark.parametrize


def enable_none() -> Any:
    env1 = {
        "DD_TRACE_PROPAGATION_STYLE_EXTRACT": "NoNe",
        "DD_TRACE_PROPAGATION_STYLE_INJECT": "none",
    }
    env2 = {
        "DD_TRACE_PROPAGATION_STYLE": "NONE",
    }
    return parametrize("library_env", [env1, env2])


def enable_none_invalid() -> Any:
    env1 = {
        "DD_TRACE_PROPAGATION_STYLE_EXTRACT": "NoNe,Datadog",
        "DD_TRACE_PROPAGATION_STYLE_INJECT": "none,Datadog",
    }
    env2 = {
        "DD_TRACE_PROPAGATION_STYLE": "NONE,Datadog",
    }
    return parametrize("library_env", [env1, env2])


@enable_none()
@pytest.mark.skip_library("golang", "not implemented")
@pytest.mark.skip_library("nodejs", "TODO: remove when https://github.com/DataDog/dd-trace-js/pull/2477 lands")
def test_headers_none_extract(test_agent, test_library):
    """Ensure that no distributed tracing headers are extracted.
    """
    with test_library:
        headers = make_single_request_and_get_inject_headers(
            test_library,
            [
                ["x-datadog-trace-id", "123456789"],
                ["x-datadog-parent-id", "987654321"],
                ["x-datadog-sampling-priority", "2"],
                ["x-datadog-origin", "synthetics"],
                ["x-datadog-tags", "_dd.p.dm=-4"],
            ],
        )

    span = get_span(test_agent)
    assert span.get("trace_id") != 123456789
    assert span.get("parent_id") != 987654321
    assert span["meta"].get(ORIGIN) is None
    assert span["meta"].get("_dd.p.dm") != "-4"
    assert span["metrics"].get(SAMPLING_PRIORITY_KEY) != 2


@enable_none_invalid()
@pytest.mark.skip_library("golang", "not implemented")
@pytest.mark.skip_library("nodejs", "TODO: remove when https://github.com/DataDog/dd-trace-js/pull/2477 lands")
def test_headers_none_extract_with_other_propagators(test_agent, test_library):
    """Ensure that the 'none' propagator is ignored when other propagators are present.
    In this case, ensure that the Datadog distributed tracing headers are extracted
    and activated properly.
    """
    with test_library:
        headers = make_single_request_and_get_inject_headers(
            test_library,
            [
                ["x-datadog-trace-id", "123456789"],
                ["x-datadog-parent-id", "987654321"],
                ["x-datadog-sampling-priority", "2"],
                ["x-datadog-origin", "synthetics"],
                ["x-datadog-tags", "_dd.p.dm=-4"],
            ],
        )

    span = get_span(test_agent)
    assert span.get("trace_id") == 123456789
    assert span.get("parent_id") == 987654321
    assert span["meta"].get(ORIGIN) == "synthetics"
    assert span["meta"].get("_dd.p.dm") == "-4"
    assert span["metrics"].get(SAMPLING_PRIORITY_KEY) == 2


@enable_none()
@pytest.mark.skip_library("golang", "not impemented")
@pytest.mark.skip_library("nodejs", "TODO: remove when https://github.com/DataDog/dd-trace-js/pull/2477 lands")
def test_headers_none_inject(test_agent, test_library):
    """Ensure that the 'none' propagator is used and
    no Datadog distributed tracing headers are injected.
    """
    with test_library:
        headers = make_single_request_and_get_inject_headers(test_library, [])

    assert "traceparent" not in headers
    assert "tracestate" not in headers
    assert "x-datadog-trace-id" not in headers
    assert "x-datadog-parent-id" not in headers
    assert "x-datadog-sampling-priority" not in headers
    assert "x-datadog-origin" not in headers
    assert "x-datadog-tags" not in headers


@enable_none_invalid()
@pytest.mark.skip_library("golang", "not impemented")
@pytest.mark.skip_library("nodejs", "TODO: remove when https://github.com/DataDog/dd-trace-js/pull/2477 lands")
def test_headers_none_inject_with_other_propagators(test_agent, test_library):
    """Ensure that the 'none' propagator is ignored when other propagators are present.
    In this case, ensure that the Datadog distributed tracing headers are injected properly.
    """
    with test_library:
        headers = make_single_request_and_get_inject_headers(test_library, [])

    span = get_span(test_agent)
    assert int(headers["x-datadog-trace-id"]) == span.get("trace_id")
    assert int(headers["x-datadog-parent-id"]) == span.get("span_id")
    assert int(headers["x-datadog-sampling-priority"]) == span["metrics"].get(SAMPLING_PRIORITY_KEY)


@enable_none()
@pytest.mark.skip_library("golang", "not implemented")
@pytest.mark.skip_library("nodejs", "TODO: remove when https://github.com/DataDog/dd-trace-js/pull/2477 lands")
def test_headers_none_propagate(test_agent, test_library):
    """Ensure that the 'none' propagator is used and
    no Datadog distributed tracing headers are extracted or injected.
    """
    with test_library:
        headers = make_single_request_and_get_inject_headers(
            test_library,
            [
                ["x-datadog-trace-id", "123456789"],
                ["x-datadog-parent-id", "987654321"],
                ["x-datadog-sampling-priority", "2"],
                ["x-datadog-origin", "synthetics"],
                ["x-datadog-tags", "_dd.p.dm=-4"],
            ],
        )

    span = get_span(test_agent)
    assert span.get("trace_id") != 123456789
    assert span.get("parent_id") != 987654321
    assert span["meta"].get(ORIGIN) is None
    assert span["meta"].get("_dd.p.dm") != "-4"
    assert span["metrics"].get(SAMPLING_PRIORITY_KEY) != 2

    assert "traceparent" not in headers
    assert "tracestate" not in headers
    assert "x-datadog-trace-id" not in headers
    assert "x-datadog-parent-id" not in headers
    assert "x-datadog-sampling-priority" not in headers
    assert "x-datadog-origin" not in headers
    assert "x-datadog-tags" not in headers

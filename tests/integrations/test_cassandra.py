# Unless explicitly stated otherwise all files in this repository are licensed under the the Apache License Version 2.0.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2021 Datadog, Inc.

from utils import weblog, interfaces, context, bug, missing_feature, scenario


@bug(library="java", reason="Endpoint is probably improperly implemented on weblog")
@missing_feature(condition=context.library != "java", reason="Endpoint is not implemented on weblog")
@scenario("INTEGRATIONS")
class Test_Cassandra:
    """ Verify that a cassandra span is created """

    def setup_main(self):
        self.r = weblog.get("/trace/cassandra")

    def test_main(self):
        interfaces.library.assert_trace_exists(self.r, span_type="cassandra")

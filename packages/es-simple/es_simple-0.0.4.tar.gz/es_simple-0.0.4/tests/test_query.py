import time
import json
import es_simple

def test_query():
    print("")
    print(json.dumps(es_simple.build_query([{"name": "tcp_rerate", "agg_func": "avg", "field": "tcp_re_rate"},
                                            {"name": "cpu", "agg_func": "max", "field": "cpu_idle"}],
                                           [
                                               {"name": "ts", "agg_type": "date_histogram"},
                                               {"name": "nodename", "agg_type": "terms", "field": "nodename",
                                                "size": 20, "order": {"tcp_rerate": "desc"}},
                                           ],
                                           "hostname:*live*", int(time.time() * 1000 - 3600 * 1000),
                                           int(time.time() * 1000), "5m", "log_timestamp", "Asia/Shanghai"), indent=4))

def test_query_builder():
    qb = es_simple.QueryBuilder("hostname:*live*", int(time.time() * 1000 - 3600 * 1000),
                                           int(time.time() * 1000))

    qb.add_metric("avg_tcp_re_rate", "avg", "tcp_re_rate")
    qb.add_metric("avg_cpu", "avg", "cpu_idle")
    qb.add_date_histogram_bucket("ts")
    qb.add_terms_bucket("nodename", "nodename", "20", {"tcp_re_rerate": "desc"})
    print("")
    print(json.dumps(qb.build(), indent=4))
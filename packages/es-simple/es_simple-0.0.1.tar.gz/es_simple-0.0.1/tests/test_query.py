import time
import json
import es_simple

def test_query():
    print("")
    print(json.dumps(es_simple.build_query([{"name": "tcp_rerate", "agg_func": "avg", "field": "tcp_re_rate"},
                                            {"name": "cpu", "agg_func": "max", "field": "cpu_idle"}],
                                           [
                                               {"name": "ts", "agg_type": "date_histogram", "field": "log_timestamp"},
                                               {"name": "nodename", "agg_type": "terms", "field": "nodename",
                                                "size": 20, "order": {"tcp_rerate": "desc"}},
                                           ],
                                           "hostname:*live*", int(time.time() * 1000 - 3600 * 1000),
                                           int(time.time() * 1000), "5m", "log_timestamp"), indent=4))
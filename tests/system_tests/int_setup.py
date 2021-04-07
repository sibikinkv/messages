import jsonconfig


def integration_test_configured(msgtype):
    with jsonconfig.Config('messages') as cfg:
        data = cfg.data
        return (
            'integration_tester' in data.keys()
            and msgtype in data['integration_tester']
        )

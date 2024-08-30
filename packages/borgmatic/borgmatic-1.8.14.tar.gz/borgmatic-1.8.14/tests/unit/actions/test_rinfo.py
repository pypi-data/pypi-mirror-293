from flexmock import flexmock

from borgmatic.actions import rinfo as module


def test_run_rinfo_does_not_raise():
    flexmock(module.logger).answer = lambda message: None
    flexmock(module.borgmatic.config.validate).should_receive('repositories_match').and_return(True)
    flexmock(module.borgmatic.borg.rinfo).should_receive('display_repository_info')
    rinfo_arguments = flexmock(repository=flexmock(), json=False)

    list(
        module.run_rinfo(
            repository={'path': 'repo'},
            config={},
            local_borg_version=None,
            rinfo_arguments=rinfo_arguments,
            global_arguments=flexmock(log_json=False),
            local_path=None,
            remote_path=None,
        )
    )


def test_run_rinfo_parses_json():
    flexmock(module.logger).answer = lambda message: None
    flexmock(module.borgmatic.config.validate).should_receive('repositories_match').and_return(True)
    flexmock(module.borgmatic.borg.rinfo).should_receive('display_repository_info').and_return(
        flexmock()
    )
    parsed_json = flexmock()
    flexmock(module.borgmatic.actions.json).should_receive('parse_json').and_return(parsed_json)
    rinfo_arguments = flexmock(repository=flexmock(), json=True)

    list(
        module.run_rinfo(
            repository={'path': 'repo'},
            config={},
            local_borg_version=None,
            rinfo_arguments=rinfo_arguments,
            global_arguments=flexmock(log_json=False),
            local_path=None,
            remote_path=None,
        )
    ) == [parsed_json]

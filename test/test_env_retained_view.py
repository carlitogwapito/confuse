import os
import unittest
from unittest.mock import patch

import confuse


class RetainedEnvViewTests(unittest.TestCase):
    def test_retained_view_follows_reload(self):
        for parse_yaml_docs in (False, True):
            with (
                self.subTest(parse_yaml_docs=parse_yaml_docs),
                patch.dict(
                    os.environ, {"VIEW_TEST_DATABASE__PORT": "4001"}, clear=True
                ),
            ):
                source = confuse.EnvSource(
                    "VIEW_TEST_", parse_yaml_docs=parse_yaml_docs
                )
                config = confuse.RootView(
                    [source, confuse.ConfigSource({"database": {"port": 4000}})]
                )
                retained = config["database"]["port"]
                assert retained.get(int) == 4001

                del os.environ["VIEW_TEST_DATABASE__PORT"]
                source.load()
                assert retained.get(int) == 4000
                assert config["database"]["port"].get(int) == 4000

                os.environ["VIEW_TEST_DATABASE__PORT"] = "4002"
                source.load()
                assert retained.get(int) == 4002
                assert config.sources[0] is source

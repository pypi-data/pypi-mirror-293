###############################################################################
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
###############################################################################

# executable test suite as per WTH, Annex A

import json
import logging
from uuid import UUID

import click

from pywis_topics.centre_id import CentreId
from pywis_topics.cli_options import cli_common_options
from pywis_topics.topics import TopicHierarchy
from pywis_topics.util import get_current_datetime_rfc3339


LOGGER = logging.getLogger(__name__)


def gen_test_id(test_id: str) -> str:
    """
    Convenience function to print test identifier as URI

    :param test_id: test suite identifier

    :returns: test identifier as URI
    """

    return f'http://wis.wmo.int/spec/wth/a/conf/core/{test_id}'


class WTHTestSuite:
    """Test suite for WIS2 Topic Hierarchy"""

    def __init__(self, data: dict):
        """
        initializer

        :param data: str of topic hierarchy

        :returns: `pywis_topics.ets.WTHTestSuite`
        """

        self.test_id = None
        self.topic = data
        self.report = []

    def run_tests(self):
        """Convenience function to run all tests"""

        results = []
        tests = []
        ets_report = {
            'summary': {},
        }

        for f in dir(WTHTestSuite):
            if all([
                    callable(getattr(WTHTestSuite, f)),
                    f.startswith('test_requirement')]):

                tests.append(f)

        for t in tests:
            results.append(getattr(self, t)())

        for code in ['PASSED', 'FAILED', 'SKIPPED']:
            r = len([t for t in results if t['code'] == code])
            ets_report['summary'][code] = r

        ets_report['tests'] = results
        ets_report['datetime'] = get_current_datetime_rfc3339()

        return {
            'ets-report': ets_report
        }

    def test_requirement_id(self):
        """
        Check for the existence of a valid id property.
        """

        status = {
            'id': gen_test_id('id'),
            'code': 'PASSED',
        }

        try:
            UUID(self.message['id'])
        except ValueError as err:
            status['code'] = 'FAILED'
            status['message'] = f'Invalid UUID: {err}'

        return status


@click.group()
def ets():
    """executable test suite"""
    pass


@click.command()
@click.pass_context
@get_cli_common_options
@click.argument('topic')
def validate(ctx, topic, logfile, verbosity):
    """validate against the abstract test suite"""

    click.echo(f'Testing {topic}')

    ts = WTHTestSuite(topic)
    try:
        results = ts.run_tests()
    except Exception as err:
        raise click.ClickException(err)

    click.echo(json.dumps(results, indent=4))
    ctx.exit(results['ets-report']['summary']['FAILED'])


ets.add_command(validate)

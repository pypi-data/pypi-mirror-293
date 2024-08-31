import logging
import re
from squad.plugins import Plugin as BasePlugin
from squad.plugins.lib.base_log_parser import BaseLogParser, REGEX_NAME, REGEX_EXTRACT_NAME

logger = logging.getLogger()

MULTILINERS = [
    ('check-kernel-exception', r'-+\[? cut here \]?-+.*?-+\[? end trace \w* \]?-+', r"\d][^\+\n]*"),
    ('check-kernel-kasan', r'=+\n\[[\s\.\d]+\]\s+BUG: KASAN:.*?=+', r"BUG: KASAN:[^\+\n]*"),
    ('check-kernel-kfence', r'=+\n\[[\s\.\d]+\]\s+BUG: KFENCE:.*?=+', r"BUG: KFENCE:[^\+\n]*"),
]

ONELINERS = [
    ('check-kernel-oops', r'^[^\n]+Oops(?: -|:).*?$', r"Oops[^\+\n]*"),
    ('check-kernel-fault', r'^[^\n]+Unhandled fault.*?$', r"Unhandled [^\+\n]*"),
    ('check-kernel-warning', r'^[^\n]+WARNING:.*?$', r"WARNING: [^\+\n]*"),
    ('check-kernel-bug', r'^[^\n]+(?: kernel BUG at|BUG:).*?$', r"BUG[^\+\n]*"),
    ('check-kernel-invalid-opcode', r'^[^\n]+invalid opcode:.*?$', r"invalid opcode: [^\+\n]*"),
    ('check-kernel-panic', r'Kernel panic - not syncing.*?$', r"Kernel [^\+\n]*"),
]

# Tip: broader regexes should come first
REGEXES = MULTILINERS + ONELINERS


class Plugin(BasePlugin, BaseLogParser):
    def __cutoff_boot_log(self, log):
        # Attempt to split the log in " login:"
        logs = log.split(' login:', 1)

        # 1 string means no split was done, consider all logs as test log
        if len(logs) == 1:
            return '', log

        boot_log = logs[0]
        test_log = logs[1]
        return boot_log, test_log

    def __kernel_msgs_only(self, log):
        kernel_msgs = re.findall(r'(\[[ \d]+\.[ \d]+\] .*?)$', log, re.S | re.M)
        return '\n'.join(kernel_msgs)

    def postprocess_testrun(self, testrun):
        if testrun.log_file is None:
            return

        boot_log, test_log = self.__cutoff_boot_log(testrun.log_file)
        logs = {
            'boot': boot_log,
            'test': test_log,
        }

        for log_type, log in logs.items():
            log = self.__kernel_msgs_only(log)
            suite, _ = testrun.build.project.suites.get_or_create(slug=f'log-parser-{log_type}')

            regex = self.compile_regexes(REGEXES)
            matches = regex.findall(log)
            snippets = self.join_matches(matches, REGEXES)

            for regex_id in range(len(REGEXES)):
                test_name = REGEXES[regex_id][REGEX_NAME]
                regex_pattern = REGEXES[regex_id][REGEX_EXTRACT_NAME]
                test_name_regex = None
                if regex_pattern:
                    test_name_regex = re.compile(regex_pattern, re.S | re.M)
                self.create_squad_tests(testrun, suite, test_name, snippets[regex_id], test_name_regex)

import os

import pylint.lint
from pylint.reporters.collecting_reporter import CollectingReporter as Reporter

from .. import viewers
from ..utils import solidipes_logging as logging
from .text import Text

logger = logging.getLogger()


class CodeSnippet(Text):
    supported_extensions = ["py", "cc", "hh", "m", "sh", "tex", "latex"]
    supported_mime_types = ["text/x-shellscript/", "text/x-tex", "text/x-script.python", "text/x-sh"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.default_viewer = viewers.Code

    def _valid_loading(self):
        self.errors = [e[1] for e in self.lint_errors]
        return super()._valid_loading()

    @Text.loadable
    def text(self):
        _text = super().text
        return _text

    @Text.cached_loadable
    def lint(self):
        fname = self.file_info.path
        lint_messages = []
        for msg in self.lint_raw:
            formatted_msg = f"{fname}:{msg['line']}:{msg['column']}:{msg['msg_id']}:{msg['symbol']}: {msg['msg']}"
            lint_messages.append((msg["msg_id"], formatted_msg))
        return lint_messages

    @Text.cached_loadable
    def lint_errors(self):
        fname = self.file_info.path
        lint_messages = []
        for msg in self.lint_raw:
            formatted_msg = f"{fname}:{msg['line']}:{msg['column']}:{msg['msg_id']}:{msg['symbol']}: {msg['msg']}"
            if msg["msg_id"][0] in ["E", "F"]:
                lint_messages.append((msg["msg_id"], formatted_msg))
        return lint_messages

    @Text.cached_loadable
    def lint_raw(self):
        logger.info(f"re-lint {self.file_info.path}")
        fname = self.file_info.path

        if os.path.splitext(fname)[1] == ".py":
            rep = Reporter()
            pylint.lint.Run([fname, "--clear-cache-post-run", "y"], reporter=rep, exit=False)
            dict_messages = []

            for message in rep.messages:
                dict_message = message.__dict__

                if "confidence" in dict_message:
                    dict_message["confidence"] = dict_message["confidence"]._asdict()

                dict_messages.append(dict_message)

            return dict_messages

        return []

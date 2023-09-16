""""
This module docs
"""

import os
from .niteru import structural_similarity


class PatternMatcher:
    """
    Class
    """
    def __init__(self):
        self.patterns_dir = '/scout/recognizer/patterns'
        self.patterns: dict[str, str] = self.load_patterns()

    def load_patterns(self):
            """
            Load html patterns from patterns repository.
            - :returns dict of html patterns and their aliases (filenames) as keys
            """
            patterns = {}
            pattern_files = os.listdir(self.patterns_dir)
            for file in pattern_files:
                path_to_file = os.path.join(self.patterns_dir, file)
                with open(path_to_file, 'r') as f:
                    patterns[file] = f.read()
            return patterns

    async def match_pattern(self, html_to_match: str) -> str:
        """
        Search which pattern matches provided html most.
        - :arg html string to match
        - :returns the alias of pattern matched most if none matched returns empty string
        """
        result = ''
        temp_max = 0
        for alias, pattern in self.patterns.items():
            sim = structural_similarity(html_to_match, pattern)
            if sim > temp_max:
                result = alias
                temp_max = sim
        return result


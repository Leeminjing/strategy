import unittest

from tools.focus_contract import parse_strategy


HEADER = '''---
schema: focus.strategy/v1
id: author/method
name: A method
version: 1.0.0
---
'''
BODY = '''
## applicability

Uncertain requirements.

## evolution

Continue existing work when possible.

## inheritance

Current constraints and evidence.
'''
VALID = HEADER + BODY


class ContractTests(unittest.TestCase):
    def test_minimal_package_and_optional_description(self):
        package = parse_strategy(VALID)
        self.assertEqual(package.metadata.id, 'author/method')
        self.assertEqual(package.metadata.description, '')
        self.assertEqual(package.strategy.evolution, 'Continue existing work when possible.')

    def test_bom_crlf_and_semver_suffix(self):
        markdown = '\ufeff' + VALID.replace('1.0.0', '2.1.0-beta.1+build.2').replace('\n', '\r\n')
        package = parse_strategy(markdown)
        self.assertEqual(package.metadata.version, '2.1.0-beta.1+build.2')
        self.assertEqual(package.strategy.inheritance, 'Current constraints and evidence.')

    def test_required_metadata_rejected_when_missing(self):
        for line in ('schema: focus.strategy/v1\n', 'id: author/method\n', 'name: A method\n', 'version: 1.0.0\n'):
            with self.subTest(line=line), self.assertRaises(ValueError):
                parse_strategy(VALID.replace(line, ''))

    def test_invalid_metadata_is_rejected(self):
        for old, new in (
            ('focus.strategy/v1', 'focus.strategy/v2'),
            ('author/method', 'Author/method'),
            ('1.0.0', '01.0.0'),
            ('A method', '"   "'),
            ('id: author/method', 'id: author/method\nunknown: value'),
            ('id: author/method', 'id: author/method\nid: author/other'),
            ('name: A method', 'name: &title A method\ndescription: *title'),
            ('name: A method', 'name: !!python/object:object {}'),
            ('name: A method', '? [complex, key]\n: value'),
        ):
            with self.subTest(new=new), self.assertRaises(ValueError):
                parse_strategy(VALID.replace(old, new))

    def test_missing_blank_and_duplicate_sections_are_rejected(self):
        for body in (
            BODY.split('## inheritance')[0],
            BODY.replace('Uncertain requirements.', '   '),
            BODY + '\n## evolution\nAnother process.\n',
            'Unsectioned prose.\n' + BODY,
        ):
            with self.subTest(body=body), self.assertRaises(ValueError):
                parse_strategy(HEADER + body)

    def test_fenced_headings_remain_body_text(self):
        for fence in ('```', '~~~~'):
            body = BODY.replace('Uncertain requirements.', f'Example:\n{fence}\n## evolution\n{fence}')
            package = parse_strategy(HEADER + body)
            self.assertIn('## evolution', package.strategy.applicability)
            self.assertEqual(package.strategy.evolution, 'Continue existing work when possible.')

    def test_section_order_is_not_fixed(self):
        package = parse_strategy(HEADER + '\n## inheritance\nEvidence.\n## evolution\nContinue.\n## applicability\nUnknown.\n')
        self.assertEqual(package.strategy.applicability, 'Unknown.')
        self.assertEqual(package.strategy.inheritance, 'Evidence.')

    def test_section_character_boundary(self):
        package = parse_strategy(VALID.replace('Uncertain requirements.', '中' * 12000))
        self.assertEqual(len(package.strategy.applicability), 12000)
        with self.assertRaises(ValueError):
            parse_strategy(VALID.replace('Uncertain requirements.', '中' * 12001))

    def test_file_utf8_byte_boundary(self):
        comment = '# ' + '🧭' * 6800
        header = HEADER.replace('name: A method', comment + '\nname: A method')
        body = '\n'.join(f'## {key}\n\n' + '🧭' * 11000 for key in ('applicability', 'evolution', 'inheritance'))
        markdown = header + body
        padding = ' ' * (160000 - len(markdown.encode('utf-8')))
        markdown = markdown.replace(comment, comment + padding)
        package = parse_strategy(markdown)
        self.assertEqual(package.metadata.id, 'author/method')
        with self.assertRaisesRegex(ValueError, '160'):
            parse_strategy(markdown.replace(comment, comment + ' '))

    def test_metadata_size_limit(self):
        large = VALID.replace('name: A method', '# ' + 'x' * 8000 + '\nname: A method')
        with self.assertRaisesRegex(ValueError, '8000'):
            parse_strategy(large)


if __name__ == '__main__':
    unittest.main()

# -*- coding: utf-8 -*-

"""test JSON cmds"""

from collections import defaultdict
import json

from .shell_test_case import  ShellTestCase


# pylint: disable=R0904
class JsonCmdsTestCase(ShellTestCase):
    """ JSON cmds tests """

    def test_json_valid(self):
        """ test valid """
        valid = '{"a": ["foo", "bar"], "b": ["foo", 3]}'
        invalid = '{"a": ["foo"'
        self.shell.onecmd("create %s/valid '%s'" % (self.tests_path, valid))
        self.shell.onecmd("create %s/invalid '%s'" % (self.tests_path, invalid))
        self.shell.onecmd("json_valid %s/valid" % (self.tests_path))
        self.shell.onecmd("json_valid %s/invalid" % (self.tests_path))
        expected_output = "yes.\nno.\n"
        self.assertEqual(expected_output, self.output.getvalue())

    def test_json_valid_recursive(self):
        """ test valid, recursively """
        valid = '{"a": ["foo", "bar"], "b": ["foo", 3]}'
        invalid = '{"a": ["foo"'
        self.shell.onecmd("create %s/valid '%s'" % (self.tests_path, valid))
        self.shell.onecmd("create %s/invalid '%s'" % (self.tests_path, invalid))
        self.shell.onecmd("json_valid %s true" % (self.tests_path))
        expected_output = "%s/valid: yes.\n%s/invalid: no.\n" % (
            self.tests_path, self.tests_path)
        self.assertEqual(expected_output, self.output.getvalue())

    def test_json_cat(self):
        """ test cat """
        jsonstr = '{"a": ["foo", "bar"], "b": ["foo", 3]}'
        self.shell.onecmd("create %s/json '%s'" % (self.tests_path, jsonstr))
        self.shell.onecmd("json_cat %s/json" % (self.tests_path))

        obj = json.loads(self.output.getvalue())

        self.assertEqual(obj["a"], ["foo", "bar"])
        self.assertEqual(obj["b"], ["foo", 3])

    def test_json_cat_recursive(self):
        """ test cat recursively """
        jsonstr = '{"a": ["foo", "bar"], "b": ["foo", 3]}'
        self.shell.onecmd("create %s/a '%s'" % (self.tests_path, jsonstr))
        self.shell.onecmd("create %s/b '%s'" % (self.tests_path, jsonstr))
        self.shell.onecmd("json_cat %s true" % (self.tests_path))

        def dict_by_path(output):
            paths = defaultdict(str)
            curpath = ""
            for line in output.split("\n"):
                if line.startswith("/"):
                    curpath = line.rstrip(":")
                else:
                    paths[curpath] += line

            for path, jstr in paths.items():
                paths[path] = json.loads(jstr)

            return paths

        by_path = dict_by_path(self.output.getvalue())

        self.assertEqual(2, len(by_path))

        for path, obj in by_path.items():
            self.assertEqual(obj["a"], ["foo", "bar"])
            self.assertEqual(obj["b"], ["foo", 3])

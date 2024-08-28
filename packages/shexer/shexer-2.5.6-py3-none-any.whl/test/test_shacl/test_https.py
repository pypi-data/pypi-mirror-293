import unittest
from shexer.shaper import Shaper
from test.const import BASE_FILES
from test.t_utils import graph_comparison_file_vs_str
import os.path as pth
from shexer.consts import SHACL_TURTLE

_BASE_DIR = BASE_FILES + "https" + pth.sep


class TestHttps(unittest.TestCase):


    def test_some_https_uris(self):
        shaper = Shaper(all_classes_mode=True,
                        graph_file_input=_BASE_DIR + "https.ttl",
                        input_format="turtle",
                        disable_comments=True,
                        )
        str_result = shaper.shex_graph(string_output=True,
                                       output_format=SHACL_TURTLE)

        self.assertTrue(graph_comparison_file_vs_str(file_path=_BASE_DIR + "https_shacl.ttl",
                                                     str_target=str_result))


#!/usr/bin/env python
"""Some tests covering the pipeline creation sub command.
"""
import os
import nf_core.create
import tempfile
import unittest


class NfcoreCreateTest(unittest.TestCase):
    def setUp(self):
        self.pipeline_name = "nf-core/test"
        self.pipeline_description = "just for 4w3s0m3 tests"
        self.pipeline_author = "Chuck Norris"
        self.pipeline_version = "1.0.0"

        self.pipeline = nf_core.create.PipelineCreate(
            name=self.pipeline_name,
            description=self.pipeline_description,
            author=self.pipeline_author,
            new_version=self.pipeline_version,
            no_git=False,
            force=True,
            outdir=tempfile.mkdtemp(),
        )

    def test_pipeline_creation(self):
        assert self.pipeline.name == self.pipeline_name
        assert self.pipeline.description == self.pipeline_description
        assert self.pipeline.author == self.pipeline_author
        assert self.pipeline.new_version == self.pipeline_version

    def test_pipeline_creation_initiation(self):
        self.pipeline.init_pipeline()
        assert os.path.isdir(os.path.join(self.pipeline.outdir, ".git"))

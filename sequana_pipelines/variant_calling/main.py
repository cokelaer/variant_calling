import sys
import os
import argparse
import shutil

from sequana.pipelines_common import SlurmOptions, Colors, SnakemakeOptions
from sequana.pipelines_common import PipelineManager

col = Colors()


class Options(argparse.ArgumentParser):
    def __init__(self, prog="variant_calling"):
        usage = col.purple(
            """This script prepares the sequana pipeline variant_calling layout to
            include the Snakemake pipeline and its configuration file ready to
            use.

            In practice, it copies the config file and the pipeline into a
            directory (variant_calling) together with an executable script

            For a local run, use :

                sequana_pipelines_variant_calling --fastq-directory PATH_TO_DATA --run-mode local

            For a run on a SLURM cluster:

                sequana_pipelines_variant_calling --fastq-directory PATH_TO_DATA --run-mode slurm

        """
        )
        super(Options, self).__init__(usage=usage, prog=prog, description="")

        # add a new group of options to the parser
        so = SlurmOptions()
        so.add_options(self)

        # add a snakemake group of options to the parser
        so = SnakemakeOptions()
        so.add_options(self)

        self.add_argument(
            "--run-mode",
            dest="run_mode",
            required=True,
            choices=['local', 'slurm'],
            help="""run_mode can be either 'local' or 'slurm'. Use local to run
                the pipeline locally, otherwise use 'slurm' to run on a cluster
                with SLURM scheduler"""
        )

        pipeline_group = self.add_argument_group("pipeline")
        pipeline_group.add_argument(
            "--output-directory",
            dest="outdir",
            default="fastqc",
            help="Where to save the FASTQC results (default fastqc/ )",
        )
        pipeline_group.add_argument(
            "--fastq-directory",
            dest="fastq_directory",
            default=".",
            required=True,
            help="Where to find the FastQ files (default current directory . ) ",
        )
        pipeline_group.add_argument(
            "--input-pattern",
            dest="input_pattern",
            default="*fastq.gz",
            help="pattern for the input FastQ files (default  *fastq.gz)",
        )
        pipeline_group.add_argument("--threads", dest="threads", default=4, type=int)

        

def main(args=None):
    NAME = "variant_calling"
    if args is None:
        args = sys.argv

    options = Options(NAME).parse_args(args[1:])

    manager = PipelineManager(options, NAME)

    # create the beginning of the command and the working directory
    manager.setup()

    # fill the config file with input parameters
    cfg = manager.config.config
    cfg.input_directory = os.path.abspath(options.bcl_directory)
    cfg.bcl2fastq.threads = options.threads
   
    manager.teardown()


if __name__ == "__main__":
    main()

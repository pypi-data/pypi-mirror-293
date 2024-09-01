import sys


def output_stdout(outputValue):
    r"""
    Outputs the value to the standard output
    :param outputValue:
    :return:
    """

    sys.stdout.write(str(outputValue))
    sys.stdout.flush()
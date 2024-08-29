# coding: utf-8

from __future__ import absolute_import
from __future__ import unicode_literals

import sys
from argparse import ArgumentParser

from .bparallel import ParallelRunner


def main():
    arg_parser = ArgumentParser(description='Запуск behave тестов'
                                            ' в параллельном режиме.')
    arg_parser.add_argument('features', type=str, nargs='+',
                            help='Список feature файлов для запуска.')
    arg_parser.add_argument('--processes', type=int, default=1,
                            help='Кол-во процессов для параллельного запуска.'
                            ' По умолчаиню равен 1')
    runner_opt, behave_opt = arg_parser.parse_known_args()
    runner_opt = vars(runner_opt)

    runner = ParallelRunner(
        runner_opt['processes'],
        runner_opt['features'],
        behave_opt
    )

    return runner.run()


if __name__ == '__main__':
    sys.exit(main())

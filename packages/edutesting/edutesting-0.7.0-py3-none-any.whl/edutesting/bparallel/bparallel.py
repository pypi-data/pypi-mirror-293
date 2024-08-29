# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import os
import re
import time
import datetime
import six.moves.queue

from multiprocessing import Process, Manager
from subprocess import call
from django.conf import settings
from six.moves import range


class ParallelRunner(object):
    u"""
    Класс для параллельного запуска тестов написанных на фреймворке behave.
     Параллельный запуск осущ. на уровне feature файлов.
    """

    features_queue = Manager().JoinableQueue()
    test_result = Manager().list()

    def __init__(self, processes_amount, features_list, behave_options):
        self.procs = processes_amount
        self.f_list = features_list
        self.behave_options = behave_options
        self.logs_path = os.path.join(settings.LOG_PATH, 'test_logs')
        if not os.path.exists(self.logs_path):
            os.mkdir(self.logs_path)

    def call_behave(self, feature_path):
        """
        Запускает behave для выполнения тестов в файле feature_path.
        :param feature_path: Полное имя feature файла
        :return: Результат выполнения комманды.
        """
        log_file = os.path.join(self.logs_path, feature_path.split('/')[-1])
        log = open(log_file, 'w+')
        behave_command = [
            'xvfb-run', '-a', '-s',
            "-screen 0, 1280x1024x8",
            'behave', feature_path
        ] + self.behave_options
        res = call(behave_command, stdout=log)
        log.close()
        return 'passed' if res == 0 else 'failed'

    def worker(self):
        """
        Подпроцес который будет запускать behave для выполнения тестов пока
        очередь self.features_queue не пуста.
        """
        while True:
            try:
                feature = self.features_queue.get_nowait()
            except six.moves.queue.Empty:
                break

            start_time = time.time()
            result = self.call_behave(feature)
            self.test_result.append(result)
            end_time = time.time()
            print(
                "Scenario {0} is complite. Took: {1}. Feature is {2}".format(
                    feature.split('/')[-1],
                    str(datetime.timedelta(seconds=end_time - start_time)),
                    result
                )
            )

    def run(self):
        u"""
        Метод для запуска процессов. Запускает кол-во процессов равное
        self.procs и после их завершения выводит отчет.
        :return: Возвращает 0 если все feature файлы успешно выполнены иначе 1.
        """
        for f in self.get_feature_files():
            self.features_queue.put(f)

        main_start_time = time.time()
        print("Begin scenarios execution at {0}".format(
            time.strftime('%H:%M:%S')))

        workers = []
        for i in range(0, self.procs):
            p = Process(target=self.worker)
            workers.append(p)
            p.start()
        [i.join() for i in workers]

        main_end_time = time.time()
        print("End scenarios execution at {0}".format(
            time.strftime('%H:%M:%S')))
        result = main_end_time - main_start_time
        print("Took: " + str(datetime.timedelta(seconds=result)))

        return_code = 0
        if any([r == 'failed' for r in self.test_result]):
            return_code = 1
        return return_code

    def get_feature_files(self):
        """
        На основе self.f_list формируем список features файлов для выполнения.
        self.f_list список который может содержать как имена feature файлов,
        так и директории с ними.
        :return: Список с полными именами feature файлов.
        """
        features_files = []
        base_dir = os.getcwd()
        for f in self.f_list:
            if not os.path.isabs(f):
                f = os.path.join(base_dir, f)
            if os.path.isfile(f):
                features_files.append(f)
            else:
                pattern = re.compile("^[\w.]+.feature$")
                files = os.listdir(f)
                features_files += (
                    [os.path.join(f, i) for i in files if pattern.match(i)])

        features_files.sort()
        return features_files

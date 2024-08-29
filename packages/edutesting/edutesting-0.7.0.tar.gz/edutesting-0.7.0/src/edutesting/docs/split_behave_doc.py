# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals

from argparse import ArgumentParser
import six


files_name = {
    'steps.edutesting.ui_steps.desktop_steps': 'Шаги для работы с рабочим столом',
    'steps.edutesting.ui_steps.field_steps': 'Шаги для работы с полями формы',
    'steps.edutesting.ui_steps.grid_steps': 'Шаги для работы с гридами',
    'steps.edutesting.ui_steps.helpers': 'Вспомогательные шаги',
    'steps.edutesting.ui_steps.login': 'Шаги для авторизации',
    'steps.edutesting.ui_steps.ui': 'Не отсортированные по категориям шаги',
    'steps.factory_steps': 'Шаги для создание тестовых данных',
    'steps.journal': 'Шаги для Классного журнала (ЭШ)',
    'steps.edo': 'Шаги ЭДО',
    'steps.personal_area_steps': 'Шаги для работы с интерфейсом ученика',
}


def chagen_docid(file_str, docid):
    res = []
    index = docid[6:]
    for l in file_str:
        if docid in l:
            l = l.replace(docid, files_name[docid])
        if index in l:
            l = l.replace(index, files_name[docid])
        res.append(l)
    return res


def create_rst_file(lines, docid):
    fname = files_name.get(docid, None)
    if fname:
        lines = chagen_docid(lines, docid)
        with open('.'.join((fname, 'rst',)), 'w') as f:
            f.write('\n'.join(lines))


def replace_gherkin_steps(line):
    gherkin_steps = {
        'Given': 'Дано',
        'When': 'Когда',
        'Then': 'То',
    }
    for k, v in six.iteritems(gherkin_steps):
        if k in line:
            line = line.replace(k, v)
    return line


def main(file_with_doc):
    with open(file_with_doc) as f:
        lines = f.read()

    docid = ''
    doc = []
    for line in lines.split('\n'):
        if line.startswith(':Module:') or line.startswith(':Filename:'):
            continue

        if line.startswith('.. _docid'):
            docid = line[9:].strip('.:')

        line = replace_gherkin_steps(line)

        if line.startswith('# -- DOCUMENT-END'):
            create_rst_file(doc, docid)
            doc = []
            continue

        doc.append(line)

if __name__ == '__main__':
    arg_parser = ArgumentParser()
    arg_parser.add_argument('--step-doc', type=str, default='')
    args = vars(arg_parser.parse_args())
    main(args['step_doc'])

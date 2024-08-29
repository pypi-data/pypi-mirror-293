/**
*  Набор функций необходимых
*  для тестирования журнала
*/

journal = (function(Ext) {

    var Journal = {
        Ext: Ext,

        /* даты в формате mm.dd.yyyy*/
        SUBPERIOD_INTERVAL: {
            '1 Четверть': {
                "from": '09.01.2014',
                "to": '10.01.2014',
            },
            '2 Четверть': {
                "from": '10.02.2014',
                "to": '12.31.2014',
            },
            '3 Четверть': {
                "from": '01.01.2015',
                "to": '03.01.2015',
            },
            '4 Четверть': {
                "from": '03.02.2015',
                "to": '05.31.2015',
            },
            '1 Полугодие': {
                "from": '01.09.2015',
                "to": '28.12.2015',
            },
            '2 Полугодие': {
                "from": '01.01.2016',
                "to": '25.06.2016',
            },
        },

        /**
        * Проверка отображения учеников в журнале
        * in: id окна журнала
        * return: boolean
        */
        is_pupil_list_displayed: function(grid_id) {
            var win = this.Ext.getCmp(grid_id);
            return win.store.data.items.length !== 0;
        },

        /**
        * Проверка отображения дат уроков в журнале
        * in: id окна журнала, заголовок в колонке урока(работа 
        * на уроке, диктант и т.д.)
        * return: boolean
        */
        is_lesson_date_displayed: function(grid_id, reg_ex_idx) {
            var win = this.Ext.getCmp(grid_id);
            var reg_ex_type = [/\d{2}.\d{2}/, /\d{1,2}:\d{2}/];
            var rows = win.colModel.rows[0];
            for (var i = 0; i < rows.length; i++) {
                if (reg_ex_idx == 0) {
                    if (rows[i].header.match(reg_ex_type[reg_ex_idx]) &&
                            rows[i].header.match(reg_ex_type[reg_ex_idx+1])) {
                        return true;
                    }
                } else if (reg_ex_idx == 1) {
                    if (rows[i].header.match(reg_ex_type[reg_ex_idx])) {
                        return true;
                    }
                }
            }
            return false;
        },

        /**
        * Проверка отображения оценки в окне 
        * in: id окна журнала, заголовок в колонке урока(работа 
        * на уроке, диктант и т.д.)
        * return: boolean
        */
        is_mark_on_toolbar: function(toolbar_id, mark) {
            var toolbar = this.Ext.getCmp(toolbar_id);
            var items = toolbar.items.items;
            for (var i = 0; i < items.length; i++) {
                if (items[i].text == mark) {
                    return true;
                }
            }
            return false;
        },

        /**
        * Нажатие кнопки в окне редактирование оценки
        * in: id тулбара, название кнопки
        */
        click_button: function(toolbar_id, button) {
            var toolbar = this.Ext.getCmp(toolbar_id);
            var buttons = toolbar.items.items;
            for (var i = 0; i < buttons.length; i++) {
                if (buttons[i].text == button) {
                    document.getElementById(buttons[i].id).click();
                    break;
                }
            }
        },

        /**
        * Проверка нажата ли кнопка в окне редактирвоание оценки
        * in: id тулбара, название кнопки
        */
        is_button_pressed: function(toolbar_id, button) {
            var toolbar = this.Ext.getCmp(toolbar_id);
            var buttons = toolbar.items.items;
            for (var i = 0; i < buttons.length; i++) {
                if (buttons[i].text == button) {
                    var b = document.getElementById(buttons[i].id);
                    return b.classList.contains('x-btn-pressed');
                }
            }
            return [];
        },

        /**
        * Поиск id колонки таблицы в журнале
        * in: id грида, заголовок колонки(Работа на уроке, Диктант и т.д.),
        * дата проведение урока, время проведения.
        * return: id колонки.
        */
        find_lesson_header: function(grid_id, header, date, time) {
            var grid = this.Ext.getCmp(grid_id);
            var idx_end, idx_begin = 1;
            for (j = 0; j < grid.colModel.rows[0].length; ++j) {
                if (!grid.colModel.rows[0][j].header) {
                    continue;
                }
                if (grid.colModel.rows[0][j].header.search(date) !== -1 && grid.colModel.rows[0][j].header.search(time) !== -1) {
                    idx_end = idx_begin + grid.colModel.rows[0][j].colspan;
                    break;
                } else {
                    idx_begin += grid.colModel.rows[0][j].colspan;
                }
            }
            return grid.colModel.columns[idx_end - 1].id;
        },

        /**
        * Проверят у всех ли уроков есть заданый столбец
        * in: id грида, заголовок колонки(Работа на уроке, Диктант и т.д.),
        * return: boolean
        */
        is_col_in_header: function(grid_id, col) {
            var grid = this.Ext.getCmp(grid_id);
            var columns = grid.colModel.columns,
                header_matches_count = 0;
            for (var i = 0; i < columns.length; i++) {
                if (columns[i].header == col) {
                    header_matches_count++;
                }
            }
            return (this.get_lessons_date(grid_id).length == header_matches_count);
        },

        /**
        * Возвращает массив с датами уроков из текущего открытого в браузере журнала
        * in: id грида,
        * return: массив с датами
        */
        get_lessons_date: function(grid_id) {
            var grid = this.Ext.getCmp(grid_id);
            var lessons_date = [],
                time_reg = /[0-9]{1,2}:[0-9]{2}/,
                rows = grid.colModel.rows[0];
            for (var i = 0; i < rows.length; i++) {
                if (time_reg.exec(rows[i].header)) {
                    lessons_date.push(rows[i].header);
                }
            }
            return lessons_date;
        },

        /**
        * Проверяем все ли даты уроков попадают в период обучения
        * in: id грида, период обучения
        * return: boolean
        */
        dates_in_period: function(grid_id, period) {
            var dates = this.get_lessons_date(grid_id),
                cur_date = new Date(),
                year = cur_date.getFullYear();
            for (var i = 0; i < dates.length; i++ ) {
                /* Приведение к формату mm.dd.yyyy */
                var d = dates[i].trim().split(" ");
                d = d[0].trim().split(".")
                utc_date = d[1] + "." + d[0] + "." + year;

                if (Date.parse(this.SUBPERIOD_INTERVAL[period]["from"]) >= Date.parse(utc_date)
                    && Date.parse(this.SUBPERIOD_INTERVAL[period]["to"]) <= Date.parse(utc_date)) {
                    return false;
                }
            }
            return true;
        },

        find_score_type_input: function(win_id) {
           inputs = document.getElementsByClassName('x-form-text x-form-field x-form-num-field')
           for (var i=0; i < inputs.length; i++) {
                input = this.Ext.getCmp(inputs[i].id)
                if (input.name == 'mark_value') {
                    return input.id
                }
           }
           return 0;
        },
        panel_state: function(win_id, win_num) {
            var win = Ext.getCmp(win_id);
            var p = win.findByType('panel').filter(function(value) {
                if(value.title == 'ИДЗ на следующий урок') {
                        return value
                    }
            })[0];
            panel = p.items.items[1].items.items[win_num];
            return !panel.disabled;
        }
    };

    return Journal;

}(Ext));
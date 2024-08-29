
helpers = (function(Ext) {

    var Helpers = {
        Ext: Ext,

        /**
        * Поиск и выделение ячейки в журнале
        * in: id в гриде, дата проведение урока, время проведения,
        * заголовок колонки(Работа на уроке, Диктант и т.д.), имя ученика
        */
        find_and_select_row: function(grid_obj, date, time, header, pupil_name) {
            'use strict';
            var grid = Ext.getCmp(grid_obj);
            var column_index,
                column_idx = 0,
                i = 0,
                j = 0,
                rows_idx,
                col_idx,
                idx_begin = 1,
                idx_end;

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
            assert(idx_end, 'Not found ' + date);

            var columns = grid.colModel.columns.slice(idx_begin + 1, idx_end + 1);

            for (j = 0; j < columns.length; ++j) {
                if (columns[j].header.search(header) !== -1) {
                    col_idx = grid.colModel.getIndexById(columns[j].id);
                    column_index = columns[j].dataIndex;
                    break;
                }
            }
            assert(col_idx, 'Not found ' + header);

            var data = grid.store.data.items;
            var fullname_attr = 'full_name';
            if (data[0].data[fullname_attr] == undefined){
                fullname_attr = 'fullname';
            };
            for (i = 0; i < data.length; ++i) {
                var record = data[i].data[column_index];
                if (data[i].data[fullname_attr].search(pupil_name) != -1) {
                    grid.selModel.select(i, col_idx);
                    break;
                }
            }
            assert(grid.getSelectionModel().hasSelection(), 'Item not selectd');
        }
    };
    return Helpers;
}(Ext));
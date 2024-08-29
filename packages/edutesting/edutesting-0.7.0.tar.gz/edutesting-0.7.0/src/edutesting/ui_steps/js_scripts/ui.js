/**
* Набор вспомогательных функций для
* поиска окон, открытия, проверок и т.д.
*/
ui = (function(Ext) {
    var Ui = {
        Ext: Ext,

        recursemenuItem: function(obj) {
            'use strict';
            var r = {};
            if (obj && obj.items && obj.items) {
                for (var i = 0; i < obj.items.length; ++i) {
                    var local_obj = obj.items[i];
                    var local_items = [];
                    if (local_obj.menu && local_obj.menu.items) {
                        local_items = recursemenuItem(local_obj.menu.items);
                    }
                    r[local_obj.text] = {
                        'id': local_obj.id,
                        'items': local_items
                    };
                }
            }
            return r;
        },

        /**
        * Поиск id всплывающих окон
        * return: id окна
        */
       find_popup_win: function(win_obj) {
            win_obj == '' ? win_obj = undefined : win_obj;
            var windows = {};
            var items = Ext.ComponentMgr.all.items;
            for (var i = 0; i < items.length; i++) {
                if (items[i].isXType('window') ||
                    items[i].hasOwnProperty('parentWindow')) {
                    if (win_obj === items[i].title){
                        items[i].title === undefined ? title = 'Nameless' : title = items[i].title;
                        windows[title] = {
                            'id': items[i].id
                        };
                    };
                }
            }
            return windows;
        },

        find_button_into_toolbar: function(win_obj, tab_name, button_name) {
            'use strict';
            var item = 0;
            var buttons = button_name.split(' -> ');
            var tab = Ext.getCmp(win_obj).find('title', tab_name)[0];
            var items = tab.items.items[0].topToolbar.items.items;

            function get_item_by_name(items, name) {
                for (var i = 0; i < items.length; ++i) {
                    if (items[i].text === name) {
                        return items[i];
                    }
                }
                return 0;
            }

            for (var j = 0; j < buttons.length; ++j) {
                item = get_item_by_name(items, buttons[j]);
                if (j != buttons.length - 1) {
                    document.getElementById(item.id).click();
                    items = item.menu.items.items;
                }
            }
            return item ? item.id : 0;
        },

        find_button_into_grid_obj: function(win_obj_id, grid_obj_id, button_name) {
            'use strict';
            var items = [];
            if (grid_obj_id) {
                items = Ext.getCmp(grid_obj_id).topToolbar.items.items;
            } else {
                var obj = Ext.getCmp(win_obj_id);
                items = obj.items.items[0].topToolbar.items.items;
            }
            var item = 0;
            var buttons = button_name.split(' -> ');

            function get_item_by_name(items, name) {
                for (var i = 0; i < items.length; ++i) {
                    if (items[i].text === name) {
                        return items[i];
                    }
                }
                return 0;
            }

            for (var j = 0; j < buttons.length; ++j) {
                item = get_item_by_name(items, buttons[j]);
                if (j != buttons.length - 1) {
                    document.getElementById(item.id).click();
                    items = item.menu.items.items;
                }
            }
            return item ? item.id : 0;
        },

        find_button_into_toolbar_low_panel: function(win_obj_id, button_name) {
            'use strict';
            var obj = Ext.getCmp(win_obj_id);
            for (var j = 0; j < obj.toolbars.length; ++j) {
                var items = obj.toolbars[j].items.items;

                for (var i = 0; i < items.length; ++i) {
                    if (items[i].text === button_name) {
                        return items[i].id;
                    }
                }
            }
            return 0;
        },

        find_and_select_row_on_tab: function(win_obj, tab_name, element, column_name, one_more) {
            'use strict';
            var column_index,
                i = 0,
                j = 0,
                tab = Ext.getCmp(win_obj).find('title', tab_name)[0];
            var grid = tab.items.items[0];

            for (j = 0; j < grid.colModel.columns.length; ++j) {
                if (grid.colModel.columns[j].header === column_name) {
                    column_index = grid.colModel.columns[j].dataIndex;
                    break;
                }
            }
            assert(column_index, 'Not found ' + column_name + ' on ' + win_obj);

            var data = grid.store.data.items;
            for (i = 0; i < data.length; ++i) {
                if (data[i].data[column_index] === element) {
                    grid.getSelectionModel().selectRow(i, Boolean(one_more));
                    if (typeof grid.events.cellclick.fire !== 'undefined') {
                        grid.events.cellclick.fire(grid);
                    }
                    break;
                }
            }
            assert(grid.getSelectionModel().hasSelection(), 'Item not selectd');

        },

        define_grid: function(grid_objs, column_name) {
            for (var i = 0; i < grid_objs.length; ++i) {
                var grid = Ext.getCmp(grid_objs[i]);
                for (var j = 0; j < grid.colModel.columns.length; ++j) {
                    if (grid.colModel.columns[j].header === column_name) {
                        return [grid, grid.colModel.columns[j].dataIndex];
                    }
                }
            }
            return 0;
        },

        find_and_select_row_in_grid: function(grid_objs, element, column_name) {
            'use strict';

            var column_index, grid;
            var grid_data = this.define_grid(grid_objs, column_name);
            grid = grid_data[0];
            column_index = grid_data[1];
            assert(column_index, 'Not found ' + column_name);

            var data = grid.store.data.items;
            for (var i = 0; i < data.length; ++i) {
                if (data[i].data[column_index].toString().trim() === element) {
                    grid.getSelectionModel().selectRow(i);
                    break;
                }
            }
            assert(grid.getSelectionModel().hasSelection(), 'Item not selectd');
        },

        find_and_select_row: function(win_obj, grid_obj, element, column_name, one_more) {
            'use strict';

            var grid = [];
            if (grid_obj) {
                grid = Ext.getCmp(grid_obj);
            } else {
                grid = Ext.getCmp(win_obj).items.items[0];
            }
            var column_index,
                i = 0,
                j = 0;
            for (j = 0; j < grid.colModel.columns.length; ++j) {
                if (grid.colModel.columns[j].header.trim() === column_name) {
                    column_index = grid.colModel.columns[j].dataIndex;
                    break;
                }
            }
            assert(column_index, 'Not found ' + column_name + ' on ' + win_obj);

            var data = grid.store.data.items;
            for (i = 0; i < data.length; ++i) {
                if (data[i].data[column_index].toString().trim() === element) {
                    grid.getSelectionModel().selectRow(i, Boolean(one_more));
                    break;
                }
            }
            assert(grid.getSelectionModel().hasSelection(), 'Item not selectd');
        },

        find_and_select_node: function(win_obj, elements, column_name) {
            'use strict';
            var column_index,
                i = -1,
                j = 0,
                obj = Ext.getCmp(win_obj);
            var tree = obj.items.items[0].selModel.tree;

            for (j = 0; j < tree.columns.length; ++j) {
                if (tree.columns[j].header === column_name) {
                    column_index = tree.columns[j].dataIndex;
                    break;
                }
            }
            assert(column_index, 'Not found ' + column_name + ' on ' + win_obj);

            var node = tree.getRootNode();

            function successfull_expand(node) {
                var oChildren = node.childNodes;
                ++i;
                if (i < elements.length) {
                    for (var x = 0; x < oChildren.length; ++x) {
                        if (elements[i] == oChildren[x].attributes[column_index]) {
                            tree.getSelectionModel().select(oChildren[x]);
                            if (!oChildren[x].isLeaf()) {
                                oChildren[x].expand(false, false, successfull_expand);
                            }
                            break;
                        }
                    }
                }
                assert(tree.getSelectionModel().getSelectedNode(), 'Item not selected');
            }

            successfull_expand(node);
        },

        element_is_last: function(win_obj, parse_elements, column_name) {
            var obj = Ext.getCmp(win_obj),
                tree = obj.items.items[0].selModel.tree,
                j,
                column_index;

            for (j = 0; j < tree.columns.length; ++j) {
                if (tree.columns[j].header === column_name) {
                    column_index = tree.columns[j].dataIndex;
                    break;
                }
            }

            return tree.getSelectionModel().getSelectedNode().attributes[column_index] == parse_elements.pop();
        },

        element_is_leaf: function(win_obj) {
            'use strict';
            var obj = Ext.getCmp(win_obj);
            var tree = obj.items.items[0].selModel.tree;
            var node = tree.getSelectionModel().getSelectedNode();

            return node.isLeaf();
        },

        find_child_input_item: function(field_label, win_obj) {
            var obj = Ext.getCmp(win_obj);
            return obj.find('fieldLabel', field_label)[0].id;
        },

        find_child_input_item_with_trigger: function(field_label, win_obj) {
            var obj = Ext.getCmp(win_obj);
            field = obj.find('fieldLabel', field_label)[0];
            if (typeof(field.triggers) != 'undefined') {
                return field.triggers[1].id;
            } else {
                return field.trigger.id;
            }
        },

        find_child_input_item_trigger2: function(field_label, win_obj) {
            var obj = Ext.getCmp(win_obj);
            return obj.find('fieldLabel', field_label)[0].triggers[2].id;
        },

        find_and_select_row_with_weekday: function(grid_obj, class_name, day, time) {
            'use strict';
            var grid = Ext.getCmp(grid_obj);
            var column_index,
                column_idx = 0,
                i = 0,
                j = 0;
            for (j = 0; j < grid.colModel.columns.length; ++j) {
                if (grid.colModel.columns[j].header === class_name) {
                    column_index = grid.colModel.columns[j].dataIndex;
                    column_idx = j;
                    break;
                }
            }
            assert(column_index, 'Not found ' + class_name);

            var data = grid.store.data.items;
            for (i = 0; i < data.length; ++i) {
                var record = data[i].data[column_index];
                if (data[i].data['weekday'] === day && data[i].data['study_time'].search(time) != -1) {
                    grid.getSelectionModel().select(i, column_idx);
                    break;
                }
            }
            assert(grid.getSelectionModel().hasSelection(), 'Item not selectd');
        },

        find_and_select_row_journal: function(grid_obj, date, header, pupil_name, value, possible, time) {
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
                if (grid.colModel.rows[0][j].header.search(date) !== -1
                && grid.colModel.rows[0][j].header.search(time) !== -1) {
                    idx_end = idx_begin + grid.colModel.rows[0][j].colspan;
                    break;
                } else {
                    idx_begin += grid.colModel.rows[0][j].colspan;
                }
            }
            assert(idx_end, 'Not found ' + date);

            var columns = grid.colModel.columns.slice(idx_begin + 1, idx_end + 1);

            for (j = 0; j < columns.length; ++j) {
                if (columns[j].header === header) {
                    col_idx = grid.colModel.getIndexById(columns[j].id);
                    column_index = columns[j].dataIndex;
                    break;
                }
            }
            assert(col_idx, 'Not found ' + header);

            var data = grid.store.data.items;
            var record = [];
            if (!possible) {
                for (i = 0; i < data.length; ++i) {
                    record = data[i].data[column_index];
                    if (data[i].data['full_name'].search(pupil_name) != -1) {
                        grid.selModel.select(i, col_idx);
                        data[i].set(column_index, value);
                        break;
                    }
                }
            } else {
                for (i = 0; i < data.length; ++i) {
                    record = data[i].data[column_index];

                    if (data[i].data['full_name'].search(pupil_name) != -1 && data[i].data[column_index] === value) {
                        grid.selModel.select(i, col_idx);
                        break;
                    }
                }
            }
            assert(grid.getSelectionModel().hasSelection(), 'Item not selectd');
        },

        find_and_select_row_date: function(grid_obj, date, time) {
            'use strict';
            var grid = Ext.getCmp(grid_obj);
            var j = 0,
                idx = 2;

            for (j = 0; j < grid.colModel.rows[0].length; ++j) {
                if (!grid.colModel.rows[0][j].header) {
                    continue;
                }
                if (grid.colModel.rows[0][j].header.search(date) != -1 &&
                    grid.colModel.rows[0][j].header.search(time) != -1) {
                    break;
                }
                idx += grid.colModel.rows[0][j].colspan;
            }
            grid.events.headerdblclick.fire(grid, idx);
        },

        find_and_select_row_date_link: function(grid_obj, date, time) {
            'use strict';
            var grid = Ext.getCmp(grid_obj);
            var j = 0,
                idx = 2;

            for (j = 0; j < grid.colModel.rows[0].length; ++j) {
                if (!grid.colModel.rows[0][j].header) {
                    continue;
                }
                // TODO Завернуть это и все по файлу длинные условия в функции
                if (grid.colModel.rows[0][j].header.search(date) != -1 &&
                    grid.colModel.rows[0][j].header.search(time) != -1) {
                    break;
                }
                idx += grid.colModel.rows[0][j].colspan;
            }
            grid.events.headerclick.fire(grid, idx);
        },

        is_field_not_valid: function(field_label, win_obj) {
            var obj = Ext.getCmp(win_obj);
            field_id = obj.find('fieldLabel', field_label)[0].id;
            field = Ext.getCmp(field_id);
            return (field.el.dom.classList.contains('m3-form-invalid') === true);
        },

        find_field_value: function(field_label, win_obj) {
            var obj = Ext.getCmp(win_obj);
            field_id = obj.find('fieldLabel', field_label)[0].id;
            return Ext.getCmp(field_id).getValue();
        },

        is_field_edit: function(field_label, win_obj) {
            var obj = Ext.getCmp(win_obj);
            field = Ext.getCmp(obj.find('fieldLabel', field_label)[0].id);
            label = Ext.getDom(field.label.id);
            return (label.firstChild.style.color == "darkmagenta" || label.firstChild.style.color == "rgb(139, 0, 139");
        },

        is_record_removed: function(toolbar_id, column_name, column_value) {
            var toolbar = Ext.getCmp(toolbar_id);

            var dataIndex = '';
            for (var i = 0; i < toolbar.colModel.columns.length; i++) {
                if (toolbar.colModel.columns[i].header == column_name) {
                    dataIndex = toolbar.colModel.columns[i].dataIndex;
                    break;
                }
            }

            var data = toolbar.store.data.items;
            for (i = 0; i < data.length; ++i) {
                if (data[i].data[dataIndex].toString().trim() === column_value) {
                    return false;
                }
            }
            return true;
        },

        is_record_in_list: function(list_id, record) {
            var list = Ext.getCmp(list_id);
            var items = list.store.data.items;
            var keys_list = Object.keys(items[0].data);
            for (var i = 0; i < items.length; i++) {
                for (var j = 0; j < keys_list.length; j++) {
                    if (items[i].data[keys_list[j]] == record) {
                        return true;
                    }
                }
            }
            return false;
        },

        get_button_from_toolbar_id: function(grid_id, button_name) {
            var grid = Ext.getCmp(grid_id);
            var items = grid.toolbars[0].items.items;
            for (var i = 0; i < items.length; i++) {
                if (items[i].text === button_name) {
                    return items[i].id;
                }
            }
            return 0;
        },

        /*
        Возвращает кол-во записей в гриде
         */
        grid_records_amount: function(grid_id) {
            var grid = Ext.getCmp(grid_id);
            return grid.store.data.items.length;
        },

        grid_records_sort_info: function(grid_id) {
            var grid = Ext.getCmp(grid_id);
            if (grid.store.sortInfo !== undefined) {
                return grid.store.sortInfo;
            }
            return undefined;
        },

        /*
         Выбор всех строк в гриде
         */
        select_all_rows_in_grid: function(grid_id) {
            var grid = Ext.getCmp(grid_id);
            grid.getSelectionModel().selectAll();
        },

        /* поиск записей в полях с автокомплитом
            in: label_id - id поля, record - искомое значение
            return: boolean
         */
        is_record_in_dynamic_select: function(label_id, record) {
            var label = Ext.getCmp(label_id);
            var items = label.store.data.items;
            for (var i=0; i<items.length; i++) {
                if (items[i].data.name == record) {
                    return true;
                }
            }
            return false;
        },

        /*
            Поиск кнопок в окне не отсящихся к grid toolbar
         */
        find_single_button: function(win_id, button_name) {
            var win = Ext.getCmp(win_id);
            var buttons = [];
            buttons = buttons.concat(win.findByType('button'));
            var i;
            for (i=0; i < win.toolbars.length; i++) {
                buttons = buttons.concat(win.toolbars[i].findByType('button'));
            }
            for (i=0; i < buttons.length; i++) {
                if (buttons[i].text == button_name) {
                    return buttons[i].id;
                }
            }
            return 0;
        },

        get_list_values: function(win_id, field_name) {
            var win = Ext.getCmp(win_id);
            var field = win.find('fieldLabel', field_name)[0];
            var data = [],
                items = field.store.data.items;
            for (var i=0; i < items.length; i++) {
                data.push(items[i].data)
            }
            return data;
        }

    };

    return Ui;
}(Ext));
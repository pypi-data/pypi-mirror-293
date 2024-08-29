/**
 *  Вспомогательные функции для работы с Ext fields
 */

win_helpers = (function(Ext){
    var Win = {
        Ext: Ext,

        is_open: function(win_id) {
            var win = Ext.getCmp(win_id);
            return (Ext.isEmpty(win)) ? false : win.isVisible();
        },

        is_close: function(win_id) {
            var win = Ext.getCmp(win_id);
            return !((Ext.isEmpty(win)) ? false : win.isVisible());
        },

        get_win_panels: function(win_id) {
            var win = Ext.getCmp(win_id),
                panels = {};
            var p = win.findByType('panel').filter(
                function(val) {
                    return typeof val.title !== 'undefined'
                }
            );
            for (var i=0; i<p.length; i++) {
                key = p[i].tbarCls;
                if (typeof key == 'undefined') { key = 'x-panel-tbar'};
                if (typeof p[i].body !== 'undefined' && p[i].body.dom.firstChild.classList.contains("x-grid-panel") == true){
                    key = "x-grid-panel"
                };
                if (typeof panels[key] == 'undefined'){
                    panels[key] = []
                };
                panels[key].push(p[i].title)
            }
            return panels;
        },

        fields_without_labels: function(win_id) {
            var win = Ext.getCmp(win_id),
                fields = [],
                tmp;
            tmp = Ext.query("div[@id="+win_id+"] input[type='text']");
            for (var i=0; i<tmp.length; i++) {
                if (tmp[i].hasAttribute('id')) {
                    var f = Ext.getCmp(tmp[i].getAttribute('id'));
                    if(f !== undefined && !f.hasOwnProperty('fieldLabel') && f.hasOwnProperty('emptyText')) {
                        var is_date;
                        f.getXType() == 'm3-date' ? is_date = true : is_date = false;
                        fields.push({
                            'label': f.emptyText,
                            'id': f.id,
                            'is_date': is_date
                        });
                    }
                }
            }
            return fields;
        },

        get_win_labels: function(win_id) {
            var win = Ext.getCmp(win_id),
                fields = [],
                tmp;
            tmp = Ext.query("label", win_id);
            for (var i=0; i<tmp.length; i++) {
                if (tmp[i].hasAttribute('for')) {
                    var label = tmp[i].textContent;
                    var f = Ext.getCmp(tmp[i].getAttribute('for'));
                    var is_date;
                    f.getXType() == 'm3-date' ? is_date = true : is_date = false;
                    fields.push({
                        'label': (label[label.length - 1] === ':') ? label.slice(0, -1) : label,
                        'id': tmp[i].getAttribute('for'),
                        'is_date': is_date
                    });
                }
            }
            return fields.concat(this.fields_without_labels(win_id));
        },

        get_win_buttons: function(win_id) {
            var win = Ext.getCmp(win_id),
                buttons_obj = [],
                buttons_result = {};
            var buttons_obj = buttons_obj.concat(win.findByType('button'));
            for (var i=0; i<win.toolbars.length; i++) {
                buttons_obj = buttons_obj.concat(win.toolbars[i].findByType('button'));
            }
            for (i=0; i<buttons_obj.length; i++) {
                buttons_result[buttons_obj[i].text] = buttons_obj[i].id;
            }
            return buttons_result;
        },

        get_win_htmleditors: function(win_id) {
            var win = Ext.getCmp(win_id),
                htmleditors = {};
            for (var i=0; i<win.findByType('htmleditor').length; i++) {
                htmleditors[win.findByType('htmleditor')[i].name] =
                    win.findByType('htmleditor')[i].id;
            }
            return htmleditors;
        },

        get_tab_by_name: function(win_id, tab_name ) {
            var win = Ext.getCmp(win_id);
            return win.find('title', tab_name).shift().id;
        },

        is_tab_visible: function(win_id, tab_name) {
            var win = Ext.getCmp(win_id);
            if (win.find('title', tab_name).length !== 0) {
                return win.find('title', tab_name).pop().isVisible();
            } else {
                return false;
            }
        },

        is_tab_active: function(win_id, tab_name){
            var win = Ext.getCmp(win_id);
                tab = win.find('title', tab_name).shift();
            return !tab.disabled;
        },

        get_text: function(win_id) {
            var win = Ext.getCmp(win_id);
            if (typeof win.items.items[0] !== 'undefined') {
                return win.items.items[0].value;
            } else {
                return false;
            }
        }
    };
    return Win;
}(Ext));

field_helper = (function(Ext){
    var Field = {
        Ext: Ext,

        get_value: function(field_id) {
            var f = Ext.getCmp(field_id);
            if (typeof parseInt(f.getValue()) !== 'number') {
                return f.getValue();
            } else {
                return f.getRawValue();
            }
        },

        is_valid: function(field_id) {
            var f = Ext.getCmp(field_id);
            return f.isValid();
        },

        is_visible: function(field_id) {
            var f = Ext.getCmp(field_id);
            return f.isVisible();
        },

        is_edited: function(field_id) {
            var f = Ext.getCmp(field_id);
            return f.isDirty();
        },

        get_upload_field_name: function(field_id) {
            var f = Ext.getCmp(field_id);
            if (f.hasOwnProperty('prefixUploadField')) {
                return f.prefixUploadField + f.name;
            } else {
                return false;
            }
        },

        press_field_button: function(field_id, button_class_type) {
            var f = Ext.getCmp(field_id);
            document.getElementById(f[button_class_type].id).click();
        },

        get_trigger_by_type: function(field_id, trigger_idx) {
            var f = Ext.getCmp(field_id);
            if (f.trigger.isVisible()) {
                if (typeof f.triggers === "undefined") {
                    return f.trigger.id;
                } else if (typeof f.triggers !== "undefined") {
                    return f.triggers[trigger_idx].id;
                } else {
                    return false;
                }
            } else {
                return false;
            }
        },

        get_list_items: function(field_id) {
            var f = Ext.getCmp(field_id),
                items = f.store.data.items,
                val_key = f.store.fields.keys[1],
                result ={};
            for (var i=0; i<items.length; i++) {
                result[items[i].data[val_key]] = items[i].data.id;
            }
            return result;
        },

        get_fias_list_items: function(field_id, field_name) {
            var f = Ext.getCmp(field_id),
                items = f.store.data.items,
                result ={},
                idx = 2;

            if (field_name.indexOf('Дом') >= 0) idx = 0;

            val_key = f.store.fields.keys[idx];

            for (var i=0; i<items.length; i++) {
                result[items[i].data[val_key]] = items[i].data.id;
            }
            return result;
        },

        date_picker_min_date: function(field_id) {
            var f = Ext.getCmp(field_id);
            return Ext.getCmp(f.menu.picker.id).minDate.dateFormat('d.m.Y');
        },

        date_picker_max_date: function(field_id) {
            var f = Ext.getCmp(field_id);
            return Ext.getCmp(f.menu.picker.id).maxDate.dateFormat('d.m.Y');
        },

        set_date_in_widget: function(field_id, year, month, day) {
            var f = Ext.getCmp(field_id);
            var dp = Ext.getCmp(f.menu.picker.id);
            dp.events.select.fire(dp, new Date(year, (month - 1), day));
        },

        get_date_picker_value: function(field_id) {
            var f = Ext.getCmp(field_id);
            return Ext.getCmp(f.menu.picker.id).getValue().dateFormat('d.m.Y');
        }
    };

    return Field;
}(Ext));


/**
 *  Вспомогательные функции для работы с Ext Grid
 */
grid_helper = (function(Ext){
    var Grid = {
        Ext: Ext,

        select_all_rows: function(grid_id) {
            var grid = Ext.getCmp(grid_id);
            grid.getSelectionModel().selectAll();
        },

        /*
         Данная фун. выберет запись в гриде, при этом сохранить выделение уже
         выбранных
         */
        select_row_by_column_value: function(grid_id, row_id) {
            var grid = Ext.getCmp(grid_id),
                sm = grid.getSelectionModel(),
                selected_rows = sm.getSelections(),
                rows_idx = [],
                search_id;
            var f = function(record, id) {
                return (record.data.id == search_id);
            };
            if (selected_rows.length !== 0) {
                for (var i=0; i<selected_rows.length; i++) {
                    search_id = selected_rows[0].id;
                    rows_idx.push(grid.store.findBy(f));
                }
            }
            search_id = row_id;
            rows_idx.push(grid.store.findBy(f));
            sm.selectRows(rows_idx);
            if (typeof grid.events.cellclick.fire !== 'undefined') {
                grid.events.cellclick.fire(grid);
            }
        },

        get_grid_columns: function(grid_id) {
            var grid = Ext.getCmp(grid_id),
                cm = grid.colModel.columns;
            var columns = {};
            for (var i=0; i<cm.length; i++) {
                if (cm[i].hasOwnProperty('header')) {
                    header = cm[i].header.replace(/(<([^>]+)>)/ig,"")
                    if (columns.hasOwnProperty(header)){
                        columns[header+"-"+cm[i].dataIndex[0]] = {
                            'id': cm[i].id,
                            'dataIndex': cm[i].dataIndex
                        };
                    }
                    else {
                        columns[header] = {
                            'id': cm[i].id,
                            'dataIndex': cm[i].dataIndex
                        };
                    }
                    if(cm[i].editor) {
                            columns[header]['editorId'] = cm[i].editor.id;
                    };
                }
            }
            return columns;
        },

        strip_tags: function(str_val) {
            return str_val.replace(/(<([^>]+)>)/ig,"");
        },

        get_grid_group_columns: function(grid_id) {
            var grid = Ext.getCmp(grid_id),
                col_groups = grid.colModel.rows[0],
                cols = grid.colModel.columns,
                result_columns = {},
                col_idx = 0;

                for (var i=0; i<col_groups.length; i++) {
                    for (var j=0; j<col_groups[i].colspan; j++) {
                        var column_key;
                        column_key = grid_helper.strip_tags(cols[col_idx].header);
                        if (col_groups[i].header !== "") {
                            column_key += '-' + col_groups[i].header.replace(/(<([^>]+)>)/ig,"").replace(/(\r\n|\n|\r)/gm,"").trim().replace(/ +/, '-');
                        }
                        result_columns[column_key] = {
                            'id': cols[col_idx].id,
                            'dataIndex': cols[col_idx].dataIndex
                        };
                        if (cols[col_idx].editor !== null) {
                            result_columns[column_key]['editorId'] = cols[col_idx].editor.id;
                        }
                        col_idx++;
                    }
                }
                return result_columns;
        },

        get_rows: function(grid_id) {
            var grid = Ext.getCmp(grid_id);
            var rows = [],
                items = grid.store.data.items;
            for (var i=0; i<items.length; i++) {
                var tmp = {};
                var result_row = "";
                for (var property in items[i].data) {
                    if (items[i].data.hasOwnProperty(property)) {
                        tmp[property] = items[i].data[property];
                        if (typeof tmp[property] === 'string') {
                            /* Если столбец  содержит чекбокс, то заменим его на
                             * строку True или False в зависимост от того включен он или нет*/
                            if (tmp[property].indexOf('x-grid3-check-col-on') !== -1) {
                                tmp[property] = 'True';
                            } else if (tmp[property].indexOf('x-grid3-check-col') !== -1) {
                                tmp[property] = 'False';
                            } else {
                                tmp[property] = tmp[property].replace(/(<([^>]+)>)/ig,"");
                            }
                        }
                    }
                }
                var row_data = [],
                    idx;
                for(var col in grid.colModel.columns) {
                    idx = grid.colModel.columns[col]['dataIndex'];
                    if(tmp[idx]) {
                        row_data.push(tmp[idx]);
                    }
                }
                tmp['row'] = row_data.join(" ");
                rows.push(tmp);
            }
            return rows;
        },

        get_total_rows_len: function(grid_id) {
            var grid = Ext.getCmp(grid_id);
            return grid.store.totalLength;
        },

        get_selected_rows: function(grid_id, row_id) {
            var grid = Ext.getCmp(grid_id);
            var selected = grid.getSelectionModel().getSelections(),
                rows = [];
            if (Boolean(row_id)) {
                selected = selected.filter(
                    function(val) {
                        return val.id == Number(row_id);
                    }
                );
                return selected.length !==0 ? selected[0].data : false;
            } else {
                for (var i=0; i<selected.length; i++) {
                    rows.push(selected[i].data);
                }
            }
            return rows;
        },

        get_grid_parent_panel: function(grid_id) {
            var grid = Ext.getCmp(grid_id);
            var panel = grid.findParentByType('panel');
            if (panel) {
                if (typeof panel.title !== 'undefined') {
                    return panel.title;
                } else {
                    return this.get_grid_parent_panel(panel.id);
                }
            } else {
                return false;
            }
        },

        get_grid_panels: function(grid_id) {
            var grid = Ext.getCmp(grid_id),
                panels = {};
            if (typeof(grid.toolbars) !== 'undefined') {
                for (var i=0; i<grid.toolbars.length; i++) {
                    var type = (typeof grid.toolbars[i].pageSize !== 'undefined') ? 'paginator' : 'control';
                    panels[type] = grid.toolbars[i].id;
                }
                return panels;
            }
            return false;
        },

        get_row_id: function(grid_id, row_value) {
            var grid = Ext.getCmp(grid_id);
        },

        clear_selection: function(grid_id, row_id) {
            var grid = Ext.getCmp(grid_id),
                sm = grid.getSelectionModel();
            if (Boolean(row_id)) {
                sm.deselectRow(grid.store.find('id', Number(row_id)));
            } else {
                sm.clearSelections();
            }
        },

        findColumnIndex: function(list, header, dataIdx){
            for(var idx in list){
                if(list[idx].header == header && list[idx].dataIndex == dataIdx){
                    return idx;
                }
            }
        },
        select_cell_by_column: function(grid_id, row_id, column_data_index, column_header) {
            var grid = Ext.getCmp(grid_id),
                sm = grid.getSelectionModel(),
                row_idx = grid.store.find('id', row_id);

            var has_double_data_idx = (grid.colModel.columns.filter(
                function(col) {return col.dataIndex == column_data_index; }
                ).length > 1);

            if(has_double_data_idx){
                columns = grid.colModel.columns;
                col_idx = this.findColumnIndex(columns, column_header, column_data_index);
            }else{
                col_idx = grid.colModel.findColumnIndex(column_data_index);
            }

            if (sm.select !== undefined) {
                    sm.select(row_idx, col_idx);
            } else {
                    sm.selectRow(row_idx, col_idx);
            }

        },

        select_cell_by_row_value: function(grid_id, row_value, targe_col_idx, help_col_idx) {
            var grid = Ext.getCmp(grid_id),
                sm = grid.getSelectionModel(),
                row_idx = grid.store.find(help_col_idx, row_value),
                col_idx = grid.colModel.findColumnIndex(targe_col_idx);
                if (sm.select !== undefined) {
                    sm.select(row_idx, col_idx);
                } else {
                    sm.selectRow(row_idx);
                    grid.events.rowclick.fire(grid, row_idx);
                }
        },

        set_value_in_cell: function(grid_id, row_id, grid_data_index, value, search_data_index) {
            var grid = Ext.getCmp(grid_id);
            var elem_idx = grid.store.find('index', row_id);
            if (elem_idx === -1) {
                elem_idx = grid.store.find('id', row_id);
            }
            if (elem_idx === -1 && typeof elem_idx !== "undefined") {
                elem_idx = grid.store.find(search_data_index, row_id);
            }
            grid.store.data.items[elem_idx].set(grid_data_index, value);
        },

        get_value_from_cell: function(grid_id, row_id, grid_data_index) {
            var grid = Ext.getCmp(grid_id);
            var elem_idx = grid.store.find('index', row_id);
            if (elem_idx === -1) {
                elem_idx = grid.store.find('id', row_id);
            }
            return grid.store.data.items[elem_idx].get(grid_data_index);
        }
    };

    return Grid;
}(Ext));


/**
 *  Вспомогательные функции для работы с GridPanel
 */
grid_panel_helper = (function(Ext){
    var GridPanel = {

        get_buttons: function(panel_id) {
            var panel = Ext.getCmp(panel_id);
            var items = panel.items.items,
                buttons = {};
            for (var i=0; i<items.length; i++) {
                buttons[items[i].text] = items[i].id;
            }
            return buttons;
        },

        scroll_page: function(panel_id,direction) {
            var panel = Ext.getCmp(panel_id);
            if (typeof panel[direction] !== 'undefined') {
                panel[direction].el.dom.click();
            }
        }

    };

    return GridPanel;
}(Ext));


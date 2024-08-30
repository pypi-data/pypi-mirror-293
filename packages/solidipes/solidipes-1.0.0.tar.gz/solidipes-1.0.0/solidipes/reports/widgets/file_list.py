import fnmatch
import os
import urllib.parse

from datasize import DataSize
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode

from solidipes.loaders.file import File
from solidipes.loaders.file_sequence import FileSequence
from solidipes.loaders.mime_types import get_possible_extensions, get_possible_mimes
from solidipes.reports.widgets.utils import FileWrapper
from solidipes.utils import logging, rename_file

from .solidipes_widget import SolidipesWidget as SPW

################################################################
print = logging.invalidPrint
logger = logging.getLogger()
################################################################

error_cell_renderer = JsCode("""
    class ErrorCellRenderer {
        init(params) {
            if (!params.value) {
                this.eGui = document.createElement("span");
                this.eGui.innerText = "";
                return;
            }

            this.eGui = document.createElement("div");
            this.eGui.innerText = params.value;
        }

        getGui() {
            return this.eGui;
        }
    }
""")


url_cell_renderer = JsCode("""
    class UrlCellRenderer {
        init(params) {
            if (!params.value) {
                this.eGui = document.createElement("span");
                this.eGui.innerText = "";
                return;
            }

            this.eGui = document.createElement("a");
            this.eGui.innerText = "View File";
            this.eGui.setAttribute("href", "");

            let parentLocation = window.parent.location;
            let parentUrl = parentLocation.origin + parentLocation.pathname;
            let url = parentUrl + params.value;

            this.eGui.addEventListener("click", _ => {
                parent.window.open(url, "_self");
            });
            // Using href does not work because inside an iframe
            // this.eGui.setAttribute("href", url);
            // this.eGui.setAttribute("target", "_parent");
        }

        getGui() {
            return this.eGui;
        }
    }
""")


file_size_aggregator = JsCode("""
    function(params) {
        let totalSize = params.values.reduce((total, value) => total + value.value, 0);

        const units = ["B", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB"];
        let i = 0;
        let displaySize = totalSize;

        for (; i < units.length; i++) {
            if (displaySize < 1024) {
                break;
            }
            displaySize /= 1024;
        }

        return {
            value: totalSize,
            display: `${Math.round(displaySize * 100) / 100}${units[i]}`,
        };
    }
""")


file_size_comparator = JsCode("""
    function(value1, value2, node1, node2, isDescending) {
        return (value1?.value - value2?.value) || 1;
    }
""")


file_size_value_formatter = JsCode("""
    function(params) {
        return params.value?.display;
    }
""")


status_aggregator = JsCode("""
    function(params) {
        let valid = true;
        let message = false;

        for (let value of params.values) {
            if (value.includes("🚫")) {
                valid = false;
                params?.rowNode?.setExpanded(true);
            }
            if (value.includes("✉️")) {
                message = true;
            }
        }

        let status = valid ? "✅" : "🚫";
        if (message) {
            status += " ✉️";
        }

        return status;
    }
""")


extension_value_formatter = JsCode("""
    function(params) {
        return params.value?.current;
    }
""")


extension_cell_editor_values = JsCode("""
    function(params) {
        let initial = params.value?.initial || "";
        let possible = params.value?.possible || [];
        return possible.map(value => ({current: value, initial, possible: possible}));
    }
""")


extension_cell_editor_format_value = JsCode("""
    function(params) {
        return params?.current;
    }
""")


extension_comparator = JsCode("""
    function(value1, value2, node1, node2, isDescending) {
        return (value1?.current.localeCompare(value2?.current)) || 1;
    }
""")


class FileList(SPW):
    def __init__(self, all_found_files=[], show_curation_cols=True, **kwargs):
        super().__init__(**kwargs)
        self.file_wildcard = self.layout.text_input("Filtering file pattern", value="*")
        self.show_only_error = self.layout.checkbox("Show only files with errors")
        self.display_files(all_found_files, show_curation_cols)
        self.current_dir_layout = None

    def file_as_dict(self, e):
        path = os.path.basename(e.file_info.path)
        dir_path = os.path.dirname(e.file_info.path)
        if dir_path.startswith("." + os.sep):
            dir_path = dir_path[2:]

        dir_list = dir_path.split(os.sep)
        if dir_list == ["."]:
            dir_list = []
        dir_dict = {f"Directory_{i}": "📁 " + dir_list[i] for i in range(len(dir_list))}

        if isinstance(e.f, FileSequence):
            path = e.f.path

        if isinstance(e.f, FileSequence):
            file_size = e.total_size
        else:
            file_size = e.file_info.size

        file_type = e.file_info.type.strip()
        human_readable_file_size = f"{DataSize(file_size):.2a}"

        if e.state.valid and (not e.discussions or e.archived_discussions):
            valid = "✅"
        else:
            valid = "🚫"

        if e.discussions:
            valid += " ✉️"

        current_extension = e.file_info.extension
        possible_extensions = get_possible_extensions(e.file_info.type)
        possible_mimes = get_possible_mimes(current_extension)

        url = f"?page=display_page&file={e.path}"

        if isinstance(e.f, FileSequence):
            dir_path = os.path.dirname(e.f.path)
            encoded_paths = [urllib.parse.quote(os.path.relpath(p, dir_path)) for p in e.f._paths]
            url += f"&loader={e.f.__class__.__name__}"
            url += "&paths=" + ",".join(encoded_paths)

        file_dict = {
            "Status": valid,
            "Filename": path,
            "Path": e.file_info.path,
            "Extension": {"current": current_extension, "initial": current_extension, "possible": possible_extensions},
            "Type": {"current": file_type, "initial": file_type, "possible": possible_mimes},
            "Size": {"value": file_size, "display": human_readable_file_size},
            "Open": url,
            "Errors": "\n".join(e.errors),
        }

        file_dict.update(dir_dict)

        return file_dict

    def display_files(self, files, show_curation_cols):
        import pandas as pd

        bar = self.progress_layout.progress(0, text="Loading files")
        n_files = len(files)

        dict_files = {"root": []}
        current_dir = "root"

        for i, (full_path, f) in enumerate(files):
            percent_complete = i * 100 // n_files
            bar.progress(percent_complete + 1, text=f"Listing {full_path}")
            if isinstance(f, File) or isinstance(f, FileSequence):
                f = FileWrapper(f)
                f.state.valid = f.valid_loading

                if not fnmatch.fnmatch(f.file_info.path.lower(), self.file_wildcard):
                    logger.info(f"Exclude {f.file_info.path.lower()}")
                    continue

                if self.show_only_error and f.state.valid:
                    continue

                dict_files[current_dir].append(self.file_as_dict(f))

            else:
                pass

        for _dir, _files in dict_files.items():
            if len(_files) == 0:
                continue

            _files = pd.DataFrame(_files)

            if _files["Status"].str.contains("🚫").any():
                from solidipes.utils import remove_completed_stage

                remove_completed_stage(1)
            else:
                from solidipes.utils import add_completed_stage

                add_completed_stage(1)

            dir_columns = [col for col in _files.columns if col.startswith("Directory")]

            grid_builder = GridOptionsBuilder.from_dataframe(_files)

            grid_builder.configure_column(
                "Status",
                # Putting aggFunc=status_aggregator directly fails when editing the grid
                aggFunc="status_aggregator",
            )

            grid_builder.configure_column(
                "Path",
                hide=True,
            )

            grid_builder.configure_column(
                "Extension",
                cellEditor="agRichSelectCellEditor",
                cellEditorParams={
                    "formatValue": extension_cell_editor_format_value,
                    "values": extension_cell_editor_values,
                    "allowTyping": True,
                    "filterList": True,
                },
                comparator=extension_comparator,
                editable=True,
                valueFormatter=extension_value_formatter,
            )

            grid_builder.configure_column(
                "Type",
                cellEditor="agRichSelectCellEditor",
                cellEditorParams={
                    "formatValue": extension_cell_editor_format_value,
                    "values": extension_cell_editor_values,
                    "allowTyping": True,
                    "filterList": True,
                },
                comparator=extension_comparator,
                editable=True,
                valueFormatter=extension_value_formatter,
            )

            grid_builder.configure_column(
                "Size",
                # Putting aggFunc=file_size_aggregator directly fails when editing the grid
                aggFunc="file_size_aggregator",
                comparator=file_size_comparator,
                valueFormatter=file_size_value_formatter,
            )

            grid_builder.configure_column(
                "Open",
                cellRenderer=url_cell_renderer,
            )
            grid_builder.configure_column(
                "Errors",
                cellRenderer=error_cell_renderer,
            )

            for col in dir_columns:
                grid_builder.configure_column(
                    col,
                    hide=True,
                    rowGroup=True,
                )

            if not show_curation_cols:
                for col in ["Status", "Extension", "Type", "Open", "Errors"]:
                    grid_builder.configure_column(
                        col,
                        hide=True,
                    )
            grid_builder.configure_columns("Filename", wrapText=True)
            grid_builder.configure_columns("Errors", wrapText=True)
            grid_builder.configure_columns("Errors", autoHeight=True)

            grid_options = grid_builder.build()

            grid_options["aggFuncs"] = {
                "status_aggregator": status_aggregator,
                "file_size_aggregator": file_size_aggregator,
            }
            grid_options["autoGroupColumnDef"]["headerName"] = "Directory"
            if show_curation_cols:
                grid_options["autoSizeStrategy"] = {"type": "fitCellContents"}
                # grid_options["autoSizeStrategy"] = {"type": "fitGridWidth"}
            else:
                grid_options["autoSizeStrategy"] = {"type": "fitGridWidth"}
            # grid_options["domLayout"] = "autoHeight"  # Bugged: initial height is sometimes too small
            grid_options["groupAllowUnbalanced"] = True
            grid_options["groupDefaultExpanded"] = -1
            # if self.show_only_error:
            #    grid_options["groupDefaultExpanded"] = -1
            # elif not show_curation_cols:
            #    grid_options["groupDefaultExpanded"] = 1
            # else:
            #    grid_options["groupDefaultExpanded"] = 2
            grid_options["suppressAggFuncInHeader"] = True
            grid_return = AgGrid(_files, gridOptions=grid_options, allow_unsafe_jscode=True)

            new_grid_data = grid_return["data"]
            self.rename_files(new_grid_data)
            self.change_mime_files(new_grid_data)

        self.progress_layout.empty()

    def rename_files(self, new_grid_data):
        from streamlit.components.v1 import html

        from solidipes.reports.web_report import clear_session_state

        extensions = new_grid_data["Extension"]
        changed_extensions = extensions.apply(lambda x: x["current"] != x["initial"])
        files_to_rename = new_grid_data[changed_extensions]

        if files_to_rename.empty:
            return

        self.layout.write("Renaming files...")

        for _, file in files_to_rename.iterrows():
            current_path = file["Path"]
            new_extension = file["Extension"]["current"]
            new_path = os.path.splitext(current_path)[0] + "." + new_extension
            rename_file(current_path, new_path)

        # Reload file list
        clear_session_state()
        html("""
            <script type="text/javascript">
                window.parent.location.reload();
            </script>
        """)

    def change_mime_files(self, new_grid_data):
        from streamlit.components.v1 import html

        from solidipes.reports.web_report import clear_session_state

        new_type = new_grid_data["Type"]
        changed_type = new_type.apply(lambda x: x["current"] != x["initial"])
        files_to_retype = new_grid_data[changed_type]

        if files_to_retype.empty:
            return

        self.layout.write("Renaming files...")

        for _, file in files_to_retype.iterrows():
            from solidipes.utils import get_mimes, set_mimes

            current_path = file["Path"]
            new_mime = file["Type"]["current"]
            mimes = get_mimes()
            mimes[current_path] = new_mime
            set_mimes(mimes)

        # Reload file list
        clear_session_state()
        html("""
            <script type="text/javascript">
                window.parent.location.reload();
            </script>
        """)

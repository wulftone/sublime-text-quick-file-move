# Moves or simply renames files via a keyboard shortcut using python os and shutil modules.
# Configure the shortcut in the .sublime-keymap file of your choice.
# See keymap file included in this project for a reference.
# Currently, it only moves files to pre-existing directories.

import os
import shutil
import sublime
import sublime_plugin


class QuickFileMoveCommand(sublime_plugin.WindowCommand):

    def run(self):
        view = self.window.active_view()
        filename = view.file_name()
        self.window.show_input_panel("Move/Rename:", filename, lambda user_input: self.rename(view, filename, user_input), None, None)

    def rename(self, view, old_filename, new_filename):
        if not self.validateFileName(view, old_filename, new_filename):
            return
        if view.is_dirty():
            view.window().run_command("save")
        window = view.window()
        self.fileOperations(window, old_filename, new_filename)
        self.setSelection(view, window.active_view())

    def validateFileName(self, view, old_file, new_file):
        if len(new_file) is 0:
            sublime.error_message("Error: No new filename given.")
            return False
        if view.is_loading():
            sublime.error_message("Error: The file is still loading.")
            return False
        if view.is_read_only():
            sublime.error_message("Error: The file is read-only.")
            return False
        if(new_file == old_file):
            sublime.error_message("Error: The new file name was the same as the old one.")
            return False
        return True

    def fileOperations(self, window, old_file, new_file):
        window.run_command("close")
        shutil.move(old_file, new_file)
        window.open_file(new_file)
        if old_file.endswith(".py"):
            os.remove(old_file + "c")

    def setSelection(self, old_view, new_view):
        new_view.sel().clear()
        new_view.sel().add_all(old_view.sel())

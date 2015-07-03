import sublime, sublime_plugin
import os, fnmatch


"""
Functions
"""

"""Helper functions"""


def get_settings():
    """Load settings.

    :returns: dictionary containing settings
    """
    return sublime.load_settings("ProjectFileList.sublime-settings")


def get_setting(key, default=None):
    """Load individual setting.

    :param key: setting key to get value for
    :param default: default value to return if no value found

    :returns: value for ``key`` if ``key`` exists, else ``default``
    """
    return get_settings().get(key, default)

setting = get_setting


class ProjectFileListCommand(sublime_plugin.WindowCommand):
	def run(self, **args):
		# get settings
		saved_file = setting('saved_file')

		for folder in self.window.project_data()['folders']:
			# called by sidebar, only process specific folder
			if 'dirs' in args and folder['path'] not in args['dirs']:
				continue

			f = open(os.path.join(folder['path'], saved_file), 'w')
			for root, dirs, files in os.walk(folder['path']):

				# remove dirs matched folder_exclude_patterns
				# prevent os.walk to walk these dir
				if 'folder_exclude_patterns' in folder:
					for folder_exclude_pattern in folder['folder_exclude_patterns']:
						for rm_dir in fnmatch.filter(dirs, folder_exclude_pattern):
							dirs.remove(rm_dir)

				# remove file matched file_exclude_patterns
				if 'file_exclude_patterns' in folder:
					for file_exclude_pattern in folder['file_exclude_patterns']:
						for rm_file in fnmatch.filter(files, file_exclude_pattern):
							files.remove(rm_file)

				if saved_file in files:
					files.remove(saved_file)

				for file in files:
					f.write(os.path.join(root, file) + "\n")
			f.close()

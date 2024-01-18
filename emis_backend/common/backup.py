import sys, os
import pkgutil

class Backup(object):

    dev = True
    project_name = None

    def __init__(self, *args, settings=None, **kwargs):
        self.settings=settings
        # super().__init__(*args, **kwargs)

    @classmethod
    def check_dir(cls):
        """
        Проверка существует ли директория, если нет создаем.
        Возвращаем True
        """
        pass

    def backup(self):
        pass

if __name__ == "__main__":
    # module = importlib.import_module('./cms_redeye', './settings.SITE_PACH')
    print(locals())
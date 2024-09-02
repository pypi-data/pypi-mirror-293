from setuptools.command.install import install


class InstallCommand(install):
    user_options = install.user_options + [
        # ('someopt', None, None), # a 'flag' option
        #('someval=', None, None) # an option that takes a value
        ('gen=', None, None) # an option that takes a value
    ]

    def initialize_options(self):
        install.initialize_options(self)
        self.someopt = None
        #self.someval = None

    def finalize_options(self):
        print("value of gen is", self.gen)
        install.finalize_options(self)

    def run(self):
        global gen
        gen = self.gen # will be 1 or None
        install.run(self)
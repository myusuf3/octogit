class StubConfigParser():
    pass

    sections = {}
    was_written = False

    def write(self, file_to_write):
        self.was_written = True

    def read(self, file_name):
        pass

    def add_section(self, section):
        self.sections[section] = {}

    def set(self, section, option, value):
        if section in self.sections:
            self.sections[section][option] = value
        else:
            raise Exception("no such section %s exists" % section)

    def get(self, section , option):
        if section in self.sections:
            if option in self.sections[section]:
                return self.sections[section][option]
            else:
                raise Exception("no such option %s exists" % option)
        else:
            raise Exception("no such section %s exists" % section)

    def remove_option(self, section, option):
        if section in self.sections:
            if option in self.sections[section]:
                del self.sections[section][option]
            else:
                raise Exception("no such option %s exists" % option)
        else:
            raise Exception("no such section %s exists" % section)




# Module for populating random names

# Python imports
import random, json, site, os

# Worldnames imports
from worldnames.populatinghelpers import email_domains, letters, genders

class WorldNames:

    def __init__(self, file: str = 'worldnames/worldnames.json'):
        """

        :param file:
        """
        site_packages = site.getsitepackages()
        site_packages.append("")
        names_in_json = []
        for sp in site_packages:
            try:
                __file = open(os.path.join(sp, file))
                names_in_json = __file.readlines()[0]
                break
            except FileNotFoundError:
                pass
        if not names_in_json:
            message = (
                    "file something.json not found. Look in the following directories:\n "
                    + os.path.abspath("worldnames/worldnames.json")
                    + "\n "
                    + "\n".join(site_packages)
            )
            raise BaseException(message)
        self.names = json.loads(names_in_json)
        self.min, self.max = 0, len(self.names)-1
        self.min_gender, self.max_gender = 0, len(genders)-1
        self.min_domain, self.max_domain = 0, len(email_domains)-1

    def full_name(self) -> str:
        """

        :return:
        """
        return f"{self.first_name()} {self.last_name()}"

    def first_name(self) -> str:
        """

        :return:
        """
        random.shuffle(self.names)
        return self.names[random.randint(self.min, self.max)]

    @staticmethod
    def last_name() -> str:
        """

        :return:
        """
        _max = random.randint(3, 12)
        random.shuffle(letters)
        _last_name = "".join(letters[0:_max])
        return f"{_last_name[0].upper()}{_last_name[1::].lower()}"

    @staticmethod
    def age() -> int:
        """

        :return:
        """
        return random.randint(0, 120)

    def gender(self) -> str:
        """

        :return:
        """
        random.shuffle(genders)
        return genders[random.randint(self.min_gender, self.max_gender)]

    def email(self, _first_name:str=None, _last_name:str=None) -> str:
        """

        :param _first_name:
        :param _last_name:
        :return:
        """
        random.shuffle(email_domains)
        domain = email_domains[random.randint(self.min_domain, self.max_domain)]
        if not first_name or not last_name:
            return f"{self.first_name()}.{self.last_name()}@{domain}"
        else:
            return f"{_first_name}.{_last_name}@{domain}"

    def user(self) -> tuple:
        """

        :return:
        """
        fn, ln = self.first_name(), self.last_name()
        return fn, ln, self.gender(), self.age(), self.email(fn, ln)

world_names = WorldNames()
full_name = world_names.full_name
first_name = world_names.first_name
last_name = world_names.last_name
age = world_names.age
gender = world_names.gender
email = world_names.email
user = world_names.user

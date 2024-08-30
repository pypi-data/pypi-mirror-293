class config:
    def __init__(self, default: str = ".config"):
        """
        A simple config class, this class can be used to store config information for your program.

        :param default:
        """
        self.customAttributes: list[str] = []

        self.filePath = default

        try:
            self.load()
        except FileNotFoundError:
            self.save()

    def registerAttribute(self, key, value) -> None:
        """
        Adds key to self and saves if save arg is true.

        :param key:
        :param value:
        :return:
        """
        if not hasattr(self, key):
            setattr(self, key, value)
            self.customAttributes.append(key)

        self.save()

    def remove(self, key):
        """
        Removes key from class.

        :param key:
        :return:
        """

        if hasattr(self, key):
            delattr(self, key)
            self.customAttributes.remove(key)

            self.save()

    def get(self, key, default=None):
        if hasattr(self, key):
            return getattr(self, key)

        else:
            return default

    def load(self) -> None:
        """
        Loads config from a file.

        :return:
        """
        with open(self.filePath, "r") as f:
            rawData = f.read().splitlines()

        for line in rawData:
            key, value = line.split("=", 1)

            setattr(self, key, value)
            self.customAttributes.append(key)

    def save(self) -> None:
        """
        Saves config to a file.

        :return:
        """
        with open(self.filePath, "w") as f:
            for attr in self.customAttributes:
                value = getattr(self, attr)
                f.write(f"{attr}={value}\n")


def test():
    """
    Test function to test config class
    :return:
    """

    c = config()
    c.registerAttribute("yuh", "dah")
    print(c.yuh)
    c.remove("yuh")
    print(c.get("yuh", "key does not exist"))


if __name__ == '__main__':
    test()

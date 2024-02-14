class Utils:

    @staticmethod
    def clean_discord_username(username: str) -> str:
        """
        This static method takes a Discord username as input and returns a cleaned version of the username.
        If the discriminator is '0', it removes it from the username.
        Otherwise, it returns the original username.
        """
        username_split = username.split("#")
        if username_split[1] == "0":
            return f"@{username_split[0]}"
        else:
            return username

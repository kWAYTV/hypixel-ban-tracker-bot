class ServerSchema:
    def __init__(self, server_id: int, channel_id: int, message_id: int = None):
        self.server_id = server_id
        self.channel_id = channel_id
        self.message_id = message_id

    def __str__(self):
        return f"RepoSchema(server_id={self.server_id}, channel_id={self.channel_id}, message_id={self.message_id})"

    def __repr__(self):
        return self.__str__()
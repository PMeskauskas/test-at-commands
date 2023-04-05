class CommunicationHandler:

    def __init__(self, type, **kwargs):
        self.__client = self.__load_module(type, **kwargs)

    def __load_module(self, type, **kwargs):
        try:

            module = __import__(f'{type}')
            return module.CommunicationClient(**kwargs)
        except:
            exit("Unable to load Communication Client")

    def connect_to_server(self):
        self.__client.connect_to_server()

    def disable_modem_manager(self):
        self.__client.disable_modem_manager()

    def enable_modem_manager(self, ):
        self.__client.enable_modem_manager()

    def send_command_to_server(self, command):
        response = self.__client.send_command_to_server(command)
        return response

    def close_connection(self):
        self.__client.close_connection()

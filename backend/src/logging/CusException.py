

# Throws for Out-of-Scope File extension 
class NotValidFileExtension(Exception):
    def __init__(self, message):
        self.message = message
        super.__init__(self.message)
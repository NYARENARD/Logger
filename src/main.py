from config_vars import class_vars
from logger_class import Logger

def main():
    instance = Logger(class_vars)
    instance.setName("Logger")
    instance.start()

main()
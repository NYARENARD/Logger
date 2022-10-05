from config_vars import class_vars
from logger_class import Logger
import typespam

def main():
    instance = Logger(class_vars)
    instance.start()
    typespam.main()

main()
from threading import Thread
from config_vars import class_vars
from logger_class import Logger

def main():
    instance = Logger(class_vars)
    instance.start()

main()
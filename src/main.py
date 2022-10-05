from threading import Thread
from config_vars import class_vars
from logger_class import Logger
import typespam

def main():
    instance = Logger(class_vars)
    instance.start()
    t = Thread(target=typespam.main, args=())
    t.start()
    

main()
import logging

def hello():
    logging.warning('Watch out!')  # will print a message to the console
    logging.info('I told you so')  # will not print anything
    print('hello this is python package')
    return{"message":"your python package ready to use"}
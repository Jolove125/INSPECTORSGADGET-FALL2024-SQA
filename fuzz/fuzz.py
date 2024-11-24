# fuzz.py

import random
import string
import os
import sys
import ast
import tempfile
import logging
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'MLForensics-farzana', 'FAME-ML')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'MLForensics-farzana', 'mining')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'MLForensics-farzana', 'empirical')))

from py_parser import checkIfParsablePython, getPythonAtrributeFuncs
from mining import makeChunks
from report import Average

logging.basicConfig(
    filename='fuzz_report.log',
    filemode='w',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def random_string(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def random_filename(extension=None):
    if extension is None:
        extension = random.choice(['txt', 'py', 'csv', 'log', 'md'])
    return f"{random_string(8)}.{extension}"

def random_list(max_length=20, element_type='any'):
    length = random.randint(0, max_length)
    if element_type == 'int':
        return [random.randint(-1000, 1000) for _ in range(length)]
    elif element_type == 'float':
        return [random.uniform(-1000.0, 1000.0) for _ in range(length)]
    elif element_type == 'str':
        return [random_string(random.randint(1, 20)) for _ in range(length)]
    elif element_type == 'mixed':
        types = ['int', 'float', 'str', 'bool', 'None']
        mixed_list = []
        for _ in range(length):
            choice = random.choice(types)
            if choice == 'int':
                mixed_list.append(random.randint(-1000, 1000))
            elif choice == 'float':
                mixed_list.append(random.uniform(-1000.0, 1000.0))
            elif choice == 'str':
                mixed_list.append(random_string(random.randint(1, 20)))
            elif choice == 'bool':
                mixed_list.append(random.choice([True, False]))
            elif choice == 'None':
                mixed_list.append(None)
        return mixed_list
    else:
        return [random.choice([random.randint(-1000, 1000), random.uniform(-1000.0, 1000.0),
                              random_string(random.randint(1, 20)), True, False, None]) for _ in range(length)]

def random_ast_tree():
    choice = random.choice(['valid', 'invalid', 'None', 'random_object'])
    if choice == 'valid':
        code = f"def {random_string(5)}():\n    pass"
        try:
            return ast.parse(code)
        except Exception:
            return None
    elif choice == 'invalid':
        return "This is not an AST"
    elif choice == 'None':
        return None
    else:
        return random.randint(0, 100)

def fuzz_makeChunks():
    logging.info("Fuzzing makeChunks(the_list, size_)")
    for i in range(100):
        the_list = random_list(element_type=random.choice(['any', 'int', 'float', 'str', 'mixed']))
        size_ = random.choice([
            random.randint(-10, 10),
            None,
            "10",
            5.5,
            [1, 2, 3],
            {'size': 10},
            True,
            False
        ])
        try:
            logging.info(f"Invoking makeChunks with the_list={the_list} and size_={size_}")
            chunks = list(makeChunks(the_list, size_))
            logging.info(f"makeChunks returned {chunks}")
        except Exception as e:
            logging.error(f"makeChunks raised an exception with the_list={the_list}, size_={size_}: {e}")

def fuzz_checkIfParsablePython():
    logging.info("Fuzzing checkIfParsablePython(pyFile)")
    for i in range(100):
        pyFile = random_filename('py')
        choice = random.choice(['create_valid', 'create_invalid', 'non_existent', 'random_string', 'None', 'int'])
        if choice == 'create_valid':
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as tmp:
                tmp.write("def foo():\n    pass\n")
                tmp_path = tmp.name
            test_file = tmp_path
        elif choice == 'create_invalid':
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as tmp:
                tmp.write("def foo(:\n    pass\n") 
                tmp_path = tmp.name
            test_file = tmp_path
        elif choice == 'non_existent':
            test_file = "/non/existent/path/" + pyFile
        elif choice == 'random_string':
            test_file = random_string(15) + ".py"
        elif choice == 'None':
            test_file = None
        elif choice == 'int':
            test_file = random.randint(0, 1000)
        else:
            test_file = pyFile 

        try:
            logging.info(f"Invoking checkIfParsablePython with pyFile={test_file}")
            result = checkIfParsablePython(test_file)
            logging.info(f"checkIfParsablePython returned {result}")
        except Exception as e:
            logging.error(f"checkIfParsablePython raised an exception with pyFile={test_file}: {e}")
        finally:
            if choice in ['create_valid', 'create_invalid'] and os.path.exists(test_file):
                try:
                    os.remove(test_file)
                    logging.info(f"Deleted temporary file {test_file}")
                except Exception as cleanup_e:
                    logging.error(f"Failed to delete temporary file {test_file}: {cleanup_e}")

def fuzz_getPythonAtrributeFuncs():
    logging.info("Fuzzing getPythonAtrributeFuncs(pyTree)")
    for i in range(100):
        pyTree = random_ast_tree()
        try:
            logging.info(f"Invoking getPythonAtrributeFuncs with pyTree={pyTree}")
            result = getPythonAtrributeFuncs(pyTree)
            logging.info(f"getPythonAtrributeFuncs returned {result}")
        except Exception as e:
            logging.error(f"getPythonAtrributeFuncs raised an exception with pyTree={pyTree}: {e}")

def fuzz_getLogStatements():
    logging.info("Fuzzing getLogStatements(pyFile)")
    for i in range(100):
        pyFile = random_filename('py')
        choice = random.choice(['create_with_logs', 'create_without_logs', 'non_existent', 'random_string', 'None', 'int'])
        if choice == 'create_with_logs':
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as tmp:
                tmp.write("import logging\nlogging.info('Test log statement')\n")
                tmp_path = tmp.name
            test_file = tmp_path
        elif choice == 'create_without_logs':
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as tmp:
                tmp.write("def foo():\n    pass\n")
                tmp_path = tmp.name
            test_file = tmp_path
        elif choice == 'non_existent':
            test_file = "/non/existent/path/" + pyFile
        elif choice == 'random_string':
            test_file = random_string(15) + ".py"
        elif choice == 'None':
            test_file = None
        elif choice == 'int':
            test_file = random.randint(0, 1000)
        else:
            test_file = pyFile 

        try:
            logging.info(f"Invoking getLogStatements with pyFile={test_file}")
            getLogStatements(test_file)
            logging.info(f"getLogStatements executed successfully for pyFile={test_file}")
        except Exception as e:
            logging.error(f"getLogStatements raised an exception with pyFile={test_file}: {e}")
        finally:
            if choice in ['create_with_logs', 'create_without_logs'] and os.path.exists(test_file):
                try:
                    os.remove(test_file)
                    logging.info(f"Deleted temporary file {test_file}")
                except Exception as cleanup_e:
                    logging.error(f"Failed to delete temporary file {test_file}: {cleanup_e}")

def fuzz_Average():
    logging.info("Fuzzing Average(Mylist)")
    for i in range(100):
        Mylist = random_list(element_type=random.choice(['int', 'float', 'mixed', 'empty']))
        Mylist = random.choice([
            Mylist,
            None,
            "not a list",
            random.randint(0, 100),
            random_string(10),
            {'a': 1},
            [1, 2, 'three', None],
            []
        ])
        try:
            logging.info(f"Invoking Average with Mylist={Mylist}")
            result = Average(Mylist)
            logging.info(f"Average returned {result}")
        except Exception as e:
            logging.error(f"Average raised an exception with Mylist={Mylist}: {e}")

def main():
    logging.info("Starting fuzzing process")

    fuzz_makeChunks()
    fuzz_checkIfParsablePython()
    fuzz_getPythonAtrributeFuncs()
    fuzz_getLogStatements()
    fuzz_Average()

    logging.info("Fuzzing process completed")

if __name__ == '__main__':
    main()

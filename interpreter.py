import sys
import keyword


# Determine Purp Froge Type of an object
def typer(obj):
    try:
        return obj.typ_name
    except:
        try:
            if int(obj) == float(obj):
                return "int"
            else:
                return "flt"
        except:
            try:
                str(obj)
                return "str"
            except:
                try:
                    bool(obj)
                    return "boo"
                except:
                    return "object"


def isKey(word):
    if word in keyword.kwlist or word in ["+", "True", "False", "-", "*", "/", "**", ">", "<", "=", "<=", "==", ">=", '(', ')', 'str', 'int', 'flt', 'boo', ':', ";", "->", "by", "while", "if", "for"]:
        return True
    try:
        int(word)
        return True
    except ValueError:
        return False


def assign_type(typ):
    if typ == "int":
        return int
    elif typ == "flt":
        return float
    elif typ == "str":
        return str
    elif typ == "boo":
        return bool
    return object


# Show line wrapper
def show_line(func):
    def wrapper(*args, **kwargs):
        thing = func(*args, **kwargs)
        if show_line:
            print(args[0])
        return thing
    return wrapper


# Create matrix
def mat():
    return [[]]


# Container types
cont_types = ["list", "set", "mat", "dict"]


class Interpreter(object):

    # Create Objects Directory
    def __init__(self):
        self.objects = dict()
        self.exeStack = [] #list of tuples of ints in the form (start, end, return, type)
        self.pointer = 0

    # Create object class
    class PurpFrogeObject(object):
        def __init__(self, objects, typ, name, value=None):
            self.typ = assign_type(typ)
            self.typ_name = typ
            self.name = name
            self.hold(value)
            self.cont_typ = "variable"
            self.objects = objects

        def __str__(self):
            value_str = self.value
            if value_str is None:
                value_str = "*EMPTY*"
            if str(value_str) == str(self.get_value()) or self.typ_name == "str":
                return "{} : {} : {}".format(self.name, self.typ_name, str(value_str))
            return "{} : {} : {} : {}".format(self.name, self.typ_name, self.name_exp(), str(self.get_value()))

        # Define printable expression representation
        def name_exp(self):
            expanded = self.value.split()
            for i in range(len(expanded)):
                expanded[i] = expanded[i].split("'")
            expanded = [item for sublist in expanded for item in sublist]
            for i in range(len(expanded)):
                if expanded[i] in self.objects:
                    expanded[i - 1] = self.objects[expanded[i]].typ_name
                    expanded[i + 1] = ""
            expanded = [item for item in expanded if item]
            return " ".join(expanded)

        def size(self):
            if self.typ_name == "str":
                return len(self.value)
            print("WARNING: Variables all have size 1.")
            return 1

        @show_line
        def hold(self, value):
            if value is None:
                self.value = value
                return True
            else:
                try:
                    self.value = self.typ(value)
                    return True
                except:
                    self.type_error(value)
            return False

        @show_line
        def be(self, value):
            try:
                self.typ(eval(value))
                self.value = value
            except:
                self.type_error(value)

        def get_value(self):
            if self.value is None:
                return "*EMPTY*"
            try:
                return eval(self.value)
            except:
                return self.value

        def type_error(self, value):
            print("ERROR: {} of type {} and value of type {}".format(self.cont_typ, self.typ_name, typer(value)))
            print("Probably causes beyond the above include:")
            print("trying to initialze an object to 'be' something when an ingredient hasn't been initialized.")

    # Container Class
    class PurpFrogeContainer(PurpFrogeObject):
        def __init__(self, objects, typ, container, name, value=None):
            self.container = list()
            self.cont_typ = container
            if value is None:
                self.container = eval(container + "()")
            else:
                try:
                    self.container = eval(value)
                except:
                    print("Failed to evaluate " + value)
            self.typ = assign_type(typ)
            self.typ_name = typ
            self.name = name
            self.objects = objects
            print(self)

        def __str__(self):
            if self.cont_typ in ["set", "dict"]:
                brackets = ["{", "}"]
            else:
                brackets = ["[", "]"]
            if len(self.container):
                ans = [str(item) for item in self.container]
            else:
                ans = ["*EMPTY*"]
            ans[0] = brackets[0] + ans[0]
            ans[len(ans) - 1] = ans[len(ans) - 1] + brackets[1]
            return "{} : {} : {} : {}".format(self.name, self.typ_name, self.cont_typ, ", ".join(ans))

        def __add__(self, other):
            try:
                return self.container + other.container
            except:
                self.cont_type_error(other)
                print("Returning None")
                return None

        def get_value(self):
            return self.container

        def cont_type_error(self, other):
            print("ERROR: {} of type {} and {} of type {}".format(self.cont_typ, self.typ_name, other.cont_typ, other.typ_name))


        def resize(self, fin, cont=None):
            if cont is None:
                cont = self.container
            if len(cont) <= fin:
                return cont[0:fin - 1]
            # If we're adding rows to a mat, make the additions lists
            if self.cont_typ == "mat" and cont == self.container:
                return cont + [["*EMPTY*"] for i in range(fin - len(cont))]
            return cont + [["*EMPTY*"] for i in range(fin - len(cont))]

        # TODO: Add explainations about these restrictions
        # Returns true if resizeable false otherwise
        def check_resizability(self, fin, verbose=True):
            # Make sure requested size is an integer that's greater than 1
            # and of a suitable for container type
            okey_dokey = [int(fin) == float(fin), fin >= 1, cont_typ not in ["set", "dict"]]
            if sum(okey_dokey) == 3:
                return True
            if verbose:
                print("-.-")
                print("What are you trying to pull here?")
                if not okey_dokey[0]:
                    print("You can only size things to integer length!")
                if not okey_dokey[1]:
                    print("You can only size things to 1 or more!")
                if not okey_dokey[2]:
                    print("You can't resize a {} at all!".format(cont_typ))
            return False

        # Return the len or resize the container to the given length
        def size(self, fin=-1996):
            if self.cont_typ == "mat":
                return self.size_mat(fin)
            # If asking for the size, give it to them
            if fin == -1996:
                return len(self.container)
            if self.check_resizability(fin):
                self.container = self.resize(fin)
                return True
            return False

        # sizing a matrix is different enough for a new function
        def size_mat(self, fin):
            if len(fin) != 2:
                print("You need 2 arguments to resize a matrix (row, column)")
                return False
            check = [self.check_resizability(i, False) for i in [0, 1]]
            if sum(check) == 2:
                # We're good to resize
                self.conatiner = [self.resize(fin[1], i) for i in self.resize(fin[0])]
                return True
            else:
                if not check[0]:
                    print("ERROR: Row index has problems.")
                    self.check_resizability(fin[0])
                if not check[1]:
                    print("ERROR: Column index has problems.")
                    self.check_resizability(fin[1])
            return False

        # hold just means do it
        @show_line
        def hold(self, obj, location="end"):
            if typer(obj) != self.typ:
                try:
                    self.cont_type_error(obj)
                except:
                    self.type_error(obj)
                return False
            checker = [int(location) == float(location), location > -1]
            if location == "end":
                self.container.append(obj)
                return True
            if sum(checker) == 2:
                self.container.insert(obj, location)
                return True
            if not checker[0]:
                print("Index needs to be an integer!")
            if not checker[1]:
                print("Index needs to be 0 or higher!")

    # Create a New Objects
    def create(self, inpt):
        if inpt[1] in cont_types:
            newobj = self.PurpFrogeContainer(self.objects, *inpt)
        else:
            newobj = self.PurpFrogeObject(self.objects, *inpt)
        self.objects[newobj.name] = newobj

    # Create a python expression from a purp froge expression
    def create_exp(self, string, operation="Eval"):
        if string.find("(") > 0:
            string = self.chunk_by_paren(string, operation)
        try:
            stringy = string.split()
        except:
            return string
        if len(stringy) == 1:
            return stringy[0]

        quote = False
        indent_over = False

        for i in range(len(stringy)):
            if not isKey(stringy[i]):
                indent_over = True
                if stringy[i] in self.objects:  # If reference to object replace with python object
                    if operation == "size":
                        stringy[i] = 'self.objects["' + stringy[i] + '"].size()'
                    else:
                        stringy[i] = 'self.objects["' + stringy[i] + '"].get_value()'
                    if stringy[i - 1] in cont_types:
                        stringy[i - 2] = ""
                    stringy[i - 1] = ""
                elif stringy[i] == '"':  # Check if we are in the middle of a quote
                    if quote:
                        quote = False
                    else:
                        quote = True
                elif quote:  # If in a string do nothing
                    pass
                else:
                    print("Sorry did not recognize the object " + stringy[i])
                    return "''"
            elif not indent_over and stringy[i] == ">":
                stringy[i] = ""  # Remove indents from expression
        if quote:
            print("Did not find closing parenthesis.")
            return "''"
        return " ".join(stringy).strip()

    # Format the Direct Object of an operation
    def do(self, direct_obj, operation):
        ans = self.create_exp(direct_obj, operation)
        if operation in ["hold", "size"]:
            if '"' in ans[0]:
                return ans
            try:
                return eval(ans)
            except:
                print("Did not eval in DO return")
        return ans

    # Counts indents at the beginning of a line
    def count_indents(self, line):
        count = 0
        for char in line:
            if char == ">":
                count += 1
            else:
                break
        return count

    # Interpret a document
    def run(self):
        # If there is a doc, read in the doc
        if len(sys.argv) > 1:
            with open(sys.argv[1]) as f:
                content = f.readlines()
            self.content = [x.strip() for x in content if len(x.strip()) > 0]
            self.indent_count = [self.count_indents(x) for x in content]
            self.exeStack.append((0, len(content), None, "main"))

            # Read line by line with instruction control on stack
            while len(self.exeStack) > 0:

                line = content[self.pointer]
                # Prints the pointer, line number, and stack at each line.
                # print("[DEBUG]: Running line #" + str(self.pointer) + " : \"" + line[0:-1] + "\" \n\t Current stack: " + str(self.exeStack))
                self.interpret(line)  # Run the line of code

                self.pointer += 1

                # Check for control flow changes
                while (self.exeStack and self.pointer == self.exeStack[-1][1]):
                    if (self.exeStack[-1][3] == "while"):
                        while_line = content[self.exeStack[-1][0]].split()[1:-1]
                        if self.interpret(" ".join(while_line) + " ;"):
                            self.pointer = self.exeStack[-1][0] + 1
                        else:
                            self.pointer = self.exeStack.pop(-1)[2]
                    elif (self.exeStack[-1][3] == "for"):
                        #FIGURE OUT WHAT TEH HECKERS FOR LOOPS ARE TODO
                        pass
                    else:
                        self.pointer = self.exeStack.pop(-1)[2]

            print("~end of script~")
            while True:
                self.interpret(input(">"))

        else:
            print("Welcome to PurpFroge!")
            print("~~~~~~~~~~~~~~~~~~~~~")
            self.interpret("help")
            while True:
                self.interpret(input(">"))

    def run_chunk(self, chunk):
        for line in chunk:
            self.interpret(chunk)

    # Console Question?
    def console_q(self, line):
        line = line.strip()
        stop = True
        # Quit?
        if line == "quit" or line == "q":
            print("Have a nice day!")
            sys.exit()
        # Help?
        elif line == "help" or line == "h":
            print("Here are a list of basic commands:")
            print("Type 'quit' or 'q' to exit")
            print("Type 'help' or 'h' for this prompt")
            print("Type 'please show objects' to see your current objects")
            print("You can also refernce the guide for more instructions")
        # Show Objects?
        elif line == "please show objects":
            print()
            print("Current Objects:")
            print("----------------")
            for obj in self.objects:
                print(self.objects[obj])
            print("----------------")
            print()
        # Delete Objects?
        elif line == "please delete objects":
            ans = input("Are you sure you want to delete all objects? :")
            if ans == "yes" or ans == "y":
                print("All objects have been deleted.")
                self.objects = dict()
            elif ans == "no" or ans == "n":
                print("Nothing has been deleted.")
            else:
                print("Sorry I didn't get that so nothing has been deleted. Try answering yes or no next time.")
        else:
            stop = False
        return stop

    def chunk_by_paren(self, line, operation):
        try:
            start_idx = line.index("(")
            end_idx = len(line) - line[::-1].index(")")
            new_line = line[start_idx:end_idx]
            try:
                if line[start_idx - 5: start_idx - 1] == "size":
                    return self.size(new_line)
            except:
                pass
            return self.do(line[start_idx:end_idx], operation)
        except:
            return self.create_exp(line, operation)

    # Size a thing
    def size(self, line):
        quote_count = sum([1 for i in line if i == "'" or i == '"'])
        ans = (self.do(line, "size")) - quote_count
        return ans

    # For questions asked directly to console
    def computer_please(self, verb, direct_obj):
        if verb == "create":
            creation_inputs = direct_obj[0:2]
            do_idx = 2
            if direct_obj[1] in cont_types:
                creation_inputs.append(direct_obj[2])
                do_idx += 1
            try:
                new_do = " ".join(direct_obj[do_idx:])
                if new_do[0] == "(" and new_do[len(new_do)-1] == ")":
                    new_do = new_do[1:len(new_do)-1]
                print(new_do)
                value = self.do(new_do, "hold")
            except:
                value = None
            creation_inputs.append(value)
            return self.create(creation_inputs)
        elif verb == "size":
            line = " ".join(direct_obj)
            start_idx = line.index("(") + 1
            end_idx = len(line) - line[::-1].index(")") - 1
            ans = self.size(line[start_idx:end_idx])
            print("The size of {} is {}".format(line[start_idx:end_idx], ans))
            return ans

    # Find Subject Verb and DO
    def run_please_line(self, split_line):
        """
        if split_line[0][0] == "(":
            start = split_line[0]
            end = split_line[::-1][0]
            start = start[1:len(start)]
            end = end[0:len(end)-1]
            """
        please = split_line.index("please")
        if please == 0:
            self.computer_please(split_line[1], split_line[2:])
            return True
        # Break statement into subject, verb, do
        subject = split_line[0: please]
        verb = split_line[please + 1]
        direct_obj = " ".join(split_line[please + 2:])
        direct_obj = direct_obj[1: len(direct_obj) - 1].split()
        if "please" in direct_obj:
            direct_obj = self.run_please_line(direct_obj)
        direct_obj = " ".join(direct_obj)
        eval("self.objects['{}'].{}('{}')".format(subject[::-1][0], verb, self.do(direct_obj, verb)))
        return True

    def scan_for_end(self, pointer):
        end = pointer + 1
        while self.indent_count[end] > self.indent_count[pointer]:
            end += 1
        return end

    def interpret(self, line):
        # Assume legitimate instructions
        global show_line

        show_line = False
        line_len = len(line) - 1
        if line_len < 0:
            line = "q"
        # Show output?
        if line[line_len] != ";":
            show_line = True
        else:
            line_len -= 1
            line = line[0:line_len + 1]
        # Check for interpreter key words
        if self.console_q(line):
            return True
        split_line = line.split()
        conditionals = ["while", "for", "if"]
        if "range" in line:
            range_idx = split_line.index("range")
            if "->" not in line:
                print("Where is the range going? You need '->' to show me.")
                return False
            else:
                end_idx = split_line.index("->")
                split_line[end_idx] = ","
            if "by" in split_line:
                end_idx = split_line.index("by")
                split_line[end_idx] = ","

            replacement = [x for x in split_line[0: range_idx]]
            replacement.append("".join(split_line[range_idx:end_idx + 3]))
            for x in split_line[end_idx + 3: len(split_line)]:
                replacement.append(x)

            line = line[0:line.index("range")] + "".join(split_line[range_idx:end_idx +3]) + " ".join(split_line[end_idx + 3 : len(split_line)])

            if len(replacement) == 1:
                print([x for x in eval(line)])
                return True
        for key_word in conditionals:
            if key_word in line:
                if ":" not in line:
                    print("I'm not sure what you're trying to do but you said {} and you don't have a :".format(key_word))
                    return False
                end = self.scan_for_end(self.pointer)
                if key_word == "for":
                    print(line)
                    self.exeStack.append((self.pointer, end, end, "for"))
                    return True
                if key_word == "while":
                    print(line)
                    self.exeStack.append((self.pointer, end, end, "while"))
                    return True
                if self.interpret(" ".join(split_line[1:len(split_line)])):
                    print(line)
                    if ("else" in content[end].split()): # Check if there is an else
                        self.exeStack.appned((self.pointer, end, self.scan_for_end(end), "if"))
                    else:
                        self.exeStack.append((self.pointer, end, end, "if"))
                    return True
                else:
                    print(line)
                    self.pointer = end
                    if ("else" in content[end].split()): # Check if there is an else
                        self.exeStack.appned((end, self.scan_for_end(end)-1, self.scan_for_end(end), "if"))
                    return True
        # If it's an inline expression try to evaluate
        if "please" not in line and "for" not in line and "while" not in line and "if" not in line:
            try:
                translated = self.create_exp(line)
                ev = eval(translated)
                if show_line:
                    print(ev)
                return ev
            except SyntaxError:
                "Sorry I didn't understand that. Type 'h' for help or try again."
                return False
        # Find the please and run as appropriate
        try:
            if split_line[0] == "please":
                self.computer_please(split_line[1], split_line[2:])
                return True
            if self.run_please_line(split_line):
                return True
        except:
            # Apologize if misunderstanding
            print("Sorry didn't understand that. Type 'h' for help or try again.")
            return False


intr = Interpreter()
intr.run()

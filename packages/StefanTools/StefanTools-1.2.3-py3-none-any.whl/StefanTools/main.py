import json
from inputimeout import inputimeout,TimeoutOccurred
import sys
import random
import time
import string



from rich.console import Console
from rich.theme import Theme
from rich.traceback import install
from rich.text import Text
from rich.style import Style
install()
theme={"success":"bold green","failure":"bold red","warning":"bold red","celebrate":"bold yellow","debug":"bold blue",\
"info":"bold white","question":"bold magenta"}
my_theme=Theme(theme)
console=Console(theme=my_theme)



integer_limit=2**63 #9,223,372,036,854,775,808 (9223372036854775807), 292 billion years in seconds
class input():
    class int():
        @staticmethod
        def no(msg="")->list:
            if msg.endswith(": ") or msg=="":
                pass
            elif msg.endswith(":"):
                msg=msg[:-1]+": "
            elif msg.endswith(" "):
                msg=msg.rstrip()+": "
            elif not msg.endswith(": "):
                msg+=": "
            try:
                a=inputimeout(msg,timeout=integer_limit)
                a=int(a)
                return [1,a]
            except ValueError:
                return [0,a]
        @staticmethod
        def yes(msg="")->int:
            if msg.endswith(": ") or msg=="":
                pass
            elif msg.endswith(":"):
                msg=msg[:-1]+": "
            elif msg.endswith(" "):
                msg=msg.rstrip()+": "
            elif not msg.endswith(": "):
                msg+=": "
            while True:
                try:
                    console.print(msg,style="question")
                    a=inputimeout(timeout=integer_limit).strip()
                    a=int(a)
                    return a
                except ValueError:
                    print(f"Please enter a number instead of {a}.",style="failure")
                    continue
                except TimeoutOccurred:
                    continue



class data:
    @staticmethod
    def save(data,save_location):
        with open(save_location,"w") as json_file:
            json.dump(data,json_file,indent=4)
        return data
    @staticmethod
    def load(save_location):
        with open(save_location,"r") as json_file:
            data=json.load(json_file)
        return data



class format:
    class number:
        @staticmethod
        def scientificNotation(number:int):
            if number>=10**12: #10**12=1,000,000,000,000. a trillion
                return "{:.2e}".format(number).replace("+","")
            else:
                return "{:,.2f}".format(number)
        @staticmethod
        def scientific_notation(number:int):
            if number>=10**12: #10**12=1,000,000,000,000. a trillion
                return "{:.2e}".format(number).replace("+","")
            else:
                return "{:,.2f}".format(number)



class create:
    @staticmethod
    def unknown(string:str="")->str:
        characters="#$%&*?@"
        color_list=[
            "red","green","yellow","blue","magenta","cyan",
            "bright_red","bright_green","bright_yellow","bright_blue","bright_magenta","bright_cyan"
        ]

        if string=="":
            obscured_info="".join(random.choice(characters) for _ in range(random.randint(7,14)))
        else:
            disallow_previous_n=2
            if disallow_previous_n>len(string):
                disallow_previous_n=len(string)
            obscured_info=""
            prev_chars=[]
            for char in string:
                if char==" ":
                    obscured_info+=" "
                    prev_chars=[]
                else:
                    available_chars=[x for x in characters if x not in prev_chars]
                    new_char=random.choice(available_chars)
                    obscured_info+=new_char
                    prev_chars.append(new_char)
                    if len(prev_chars)>disallow_previous_n:
                        prev_chars.pop(0)


        styled_text=""
        prev_color=None
        for char in obscured_info:
            if prev_color!=None and prev_color.startswith("bright_"):
                forbidden_color=prev_color.replace("bright_","")
                #forbidden_color=prev_color.split("_")[1] #alternative way to do it
            elif prev_color!=None:
                forbidden_color="bright_"+prev_color
            else:
                forbidden_color=None

            available_colors=[color for color in color_list if color!=prev_color and color!=forbidden_color]
            color=random.choice(available_colors)
            styled_text+=f"[{color}]{char}[/]"
            prev_color=color

        return styled_text



def clear(method:int=1):
    if method==1 and not isinstance(method,bool): #The "not isinstance(method,bool)" prevents "True" from being an argument
        sys.stdout.flush()
        time.sleep(0.1)
        print("\033[2J\033[H",end="",flush=True)
        time.sleep(0.1)
        sys.stdout.flush()
    elif method==2:
        print("\033c",end="",flush=True)
    #both of the methods are copied from https://ask.replit.com/t/clear-console-in-python/65265
    else:
        raise ValueError(f"Invalid method {method}.")



class words:

    @staticmethod
    def get_final_list(initial_list:list):
        final_list=initial_list.copy()
        for element in initial_list:
            final_list.append(string.capwords(element))
            for x in ["!","?",".","!?","?!"]:
                final_list.append(element+x)
                final_list.append(string.capwords(element+x))
        return list(dict.fromkeys(final_list))

    @staticmethod
    def positive()->list:
        initial_list=["y","yes","true","i would","indeed","ofc","of course","yes of course","i guess","ig","i should",\
"i guess i would","i think i should","yes indeed","i guess i should","why not"]
        return words.get_final_list(initial_list)

    @staticmethod
    def negative()->list:
        initial_list=["n","no","false","i wouldn't","no way","not at all","nope","no thanks","i don't","i guess not","no i don't",\
"ofc not"]
        return words.get_final_list(initial_list)

    @staticmethod
    def exit()->list:
        initial_list=["exit","exit program","quit","quit program","leave","leave program","abort","abort program","home","let me out",\
"lemme out","i wanna go","i want to go","let me leave"]
        return words.get_final_list(initial_list)
    def hurry()->list:
        initial_list=["hurry","hurry up","hurry up already","hurry up already!"]
        return words.get_final_list(initial_list)



def fraction(first_number:int|float,second_number:int|float,multiply_by:int|float=1.0)->float:
    """Makes a fraction and returns it multiplied by an optional number.

    Args:
        first_number (int or float): The number in a fraction that's above.
        second_number (int or float): The number in a fraction that's below.
        multiply_by (int or float, optional): Multiply the result by this number. Defaults to 1.0.

    Returns:
        float: A fraction multiplied by an optional number.
    """

    if second_number==0:
        console.print("Cannot divide by zero.",style="failure")
        while True:
            a=inputimeout(timeout=integer_limit)
            if a=="exit":
                break

    if isinstance(first_number,str) and first_number.isdigit():
        console.print("It was probably unintentional but the first number is a string. It has been turned into an integer.")
        first_number=int(first_number)
    if isinstance(second_number,str) and second_number.isdigit():
        console.print("It was probably unintentional but the second number is a string. It has been turned into an integer.")
        second_number=int(second_number)

    return (first_number/second_number)*multiply_by



def output(text="",style:str="",end:str="\n",sep:str=" ",animation:bool=True,delay:float=0.01,use_rich:bool=True,\
delay_between_lines:float=0.0,auto_color:dict={})->None:

    """Just prints text.

    Args:
        text (optional): The text to print. If it's a list, it will be treated as if you put a comma between elements in a normal print. If it's neither a list or a string, it will be turned to a string. Defaults to "".
        style (str, optional): The style to use. Has no use if use_rich is set to False. Defaults to "".
        end (str, optional): The thing to put at the end of the text. Defaults to a new line.
        sep (str, optional): The thing that is printed between each element of the list. Is useless if text is not a list or is a list with 1 element. Defaults to " ".
        animation (bool, optional): Whether to animate the printing of the text. Defaults to True.
        delay (float, optional): The delay between printing characters. Defaults to 0.01.
        use_rich (bool, optional): Whether to use rich. Defaults to True.
        delay_between_lines (float, optional): The delay between printing elements of the list text. Is useless if text is not a list or is a list with 1 element. Defaults to 0.0.
        auto_color (dict, optional): A dictionary of words to look out for and if they are in the word, color them. \
**This may color parts of a word you maybe didn't want it to color. \
To fix that, instead of setting the value of auto_color to {"a","red"}, instead, set it to {" a ","red"}.** Defaults to {}.

    Returns:
        None (None): Nothing.

    """

    if not isinstance(text,(str,list)):
        text==str(text)


    global theme
    if style in theme:
        style:str=theme[style]
    style=style if use_rich else ""

    for try_to_find,color in auto_color.items():
        text=text.replace(try_to_find,f"[{color}]{try_to_find}[/]")

    def one_line(line:str)->None:

        if animation:


            if use_rich:
                rich_text=Text.from_markup(line)
                segments=rich_text.render(console)

                for segment in segments:
                    segment_text=segment.text
                    style_a:Style=Style.parse(style)
                    if segment.style is None:
                        segment_style:Style=style_a
                    else:
                        segment_style:Style=style_a+segment.style #Don't change the order that these 2 are being added, it's important
                    for letter in segment_text:
                        console.print(Text(letter,style=segment_style),end="")
                        time.sleep(delay)
            else:
                for letter in line:
                    print(letter,end="",flush=True)
                    time.sleep(delay)


        else:
            if use_rich:
                console.print(line,style=style,end="")
            else:
                print(line,end="")

        time.sleep(delay_between_lines)


    if isinstance(text,str):
        text=[text]


    for line in text:
        one_line(line)
        if sep!="" and len(text)>1:
            output(sep,animation=animation,style=style,end="",sep="")
    if end!="":
        output(end,animation=animation,style=style,end="")
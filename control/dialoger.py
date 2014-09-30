from __future__ import print_function
import time
import sys


def computer_talk(words, question=False, yesno=False, delay=.1):
    """Takes string at outputs it as if being typed; optionally
	handles question input and resolving yes/no answer input.
	Repeats question if answer seems not right.
	
	:param str words: the computer's voice
	:param bool question: whether this is a question
	:param bool yesno: whether question is yes or no
	:param float delay: time between character flushes
	"""

    response = None
    while response is None:
        for char in words:
            time.sleep(delay)
            print(char, end='')
            sys.stdout.flush()

        if question:
            print(' ', end='')
            if yesno:
                response = _resolve_yesno(raw_input(''))
            else:
                response = raw_input('')
        else:
            response = True
            print('')
        print('')

        if response is None or (isinstance(response, str)
                                and len(response.strip()) < 1):
            computer_talk("CANNOT... COMPUTE...")
            response = None

    return response


def _resolve_yesno(answer):
    """Resolves yes/no input: True=yes, False=no, None=invalid
	
	:param str answer: input to be analyzed for yes/no response
	"""

    answer += 'z'
    answer = answer.strip()[0].lower()
    if answer == 'y' or answer == 's':
        return True
    elif answer == 'n':
        return False
    else:
        return None

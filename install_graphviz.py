import conda.cli.python_api as Conda
import sys

###################################################################################################
# The below is roughly equivalent to:
#   conda install -y 'args-go-here' 'no-whitespace-splitting-occurs' 'square-brackets-optional'

(stdout_str, stderr_str, return_code_int) = Conda.run_command(
    Conda.Commands.INSTALL, # alternatively, you can just say "install"
                            # ...it's probably safer long-term to use the Commands class though
                            # Commands include:
                            #  CLEAN,CONFIG,CREATE,INFO,INSTALL,HELP,LIST,REMOVE,SEARCH,UPDATE,RUN
    [ 'args-go-here', 'no-whitespace-splitting-occurs', 'square-brackets-optional' ],
    use_exception_handler=True,  # Defaults to False, use that if you want to handle your own exceptions
    stdout=sys.stdout, # Defaults to being returned as a str (stdout_str)
    stderr=sys.stderr, # Also defaults to being returned as str (stderr_str)
    search_path=Conda.SEARCH_PATH  # this is the default; adding only for illustrative purposes
)
###################################################################################################



#https://stackoverflow.com/questions/41767340/using-conda-install-within-a-python-script

#import conda.cli
#conda.cli.main('conda', 'install',  '-y', 'numpy')



from colorama import Fore, Style, init

init(convert=True)

class UI:
    @classmethod
    def banner(cls):
        logo = f'''{Fore.LIGHTMAGENTA_EX} 
        ██████╗ ██╗███████╗ ██████╗ ██████╗  █████╗ ███╗   ██╗███████╗
        ██╔══██╗██║██╔════╝██╔═══██╗██╔══██╗██╔══██╗████╗  ██║██╔════╝
        ██████╔╝██║███████╗██║   ██║██████╔╝███████║██╔██╗ ██║█████╗  
        ██╔═══╝ ██║╚════██║██║   ██║██╔═══╝ ██╔══██║██║╚██╗██║██╔══╝  
        ██║     ██║███████║╚██████╔╝██║     ██║  ██║██║ ╚████║███████╗
        ╚═╝     ╚═╝╚══════╝ ╚═════╝ ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝
        {Style.RESET_ALL}'''
        print(logo)

    @classmethod
    def start_menu(cls):
        menu = f'''{Fore.LIGHTMAGENTA_EX}
        ╔══════════════════════════════╗
            [1] Start Single Account (Mailnator)
            [2] Start Multi-threaded (Mailnator)
            [3] Exit
        ╚══════════════════════════════╝{Style.RESET_ALL}
        '''
        print(menu)

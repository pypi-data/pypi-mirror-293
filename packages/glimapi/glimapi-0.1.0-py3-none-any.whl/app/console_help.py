from colorama import init, Fore, Style
from termcolor import colored

def show_help():
    init(autoreset=True)
    
    help_title = colored('Glim API Help', 'cyan', attrs=['bold'])
    overview_title = colored('Overview', 'green', attrs=['bold'])
    commands_title = colored('Commands', 'green', attrs=['bold'])
    doc_title = colored('Documentation', 'green', attrs=['bold'])

    overview_text = (
        "Glim API is a dynamic API generator with support for JWT authentication, "
        "rate limiting, and localization. This tool provides a quick and efficient way "
        "to set up a powerful API with minimal configuration."
    )

    command_generate = colored('1. Generate the Configuration File', 'yellow', attrs=['bold'])
    generate_text = (
        "To generate the `config.toml` file, which contains all the necessary settings for your API, "
        "use the following command:\n\n"
        f"{Fore.GREEN}glimapi-generate-toml{Style.RESET_ALL}\n\n"
        "This will create a `config.toml` file in your current working directory. Edit this file to configure your API according to your needs."
    )

    command_start = colored('2. Start the API Server', 'yellow', attrs=['bold'])
    start_text = (
        "Once you've configured your API, start the server using:\n\n"
        f"{Fore.GREEN}glimapi-start{Style.RESET_ALL}\n\n"
        "This command will launch the API server based on the settings defined in your `config.toml` file."
    )

    command_help = colored('3. Display This Help Message', 'yellow', attrs=['bold'])
    help_text = (
        "To display this help message again, use the following command:\n\n"
        f"{Fore.GREEN}glimapi-help{Style.RESET_ALL}"
    )

    documentation_text = (
        "For more detailed information, please refer to the official documentation or visit our website."
    )

    print(help_title)
    print()
    print(overview_title)
    print(overview_text)
    print()
    print(commands_title)
    print()
    print(command_generate)
    print(generate_text)
    print()
    print(command_start)
    print(start_text)
    print()
    print(command_help)
    print(help_text)
    print()
    print(doc_title)
    print(documentation_text)


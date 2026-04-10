from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


if __name__ == "__main__":
    from . import cli  # Before loading, must load the env
    cli.run()

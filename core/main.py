from discord import errors
from core.discordClient import mdb_client


def main():
    try:
        mdb_client.run(open("token.txt", "r").read())
    except errors.LoginFailure:
        print("Invalid token in token.txt")


if __name__ == '__main__':
    main()

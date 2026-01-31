from src.core.generator import generate_password


def main():
    password = generate_password(8,True,True,True,True)
    print(password)

if __name__ == "__main__":
    main()
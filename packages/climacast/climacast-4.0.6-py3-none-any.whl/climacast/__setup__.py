
def main():
    import os

    print("Thank you for installing my program and if you have any suggestions or questions feel free to open an issue. And if you like this program, please give it a star in github. https://github.com/shvedt/ClimaCast")

    api_key = input("Enter API key [if you don't have one, get one from OpenWeatherMap.org]: ")

    directory = os.path.join(os.getenv("HOME"), '.config', 'climacast')
    os.makedirs(directory, exist_ok=True)

    file = os.path.join(directory, 'api_key.txt')

    with open(file, 'w') as file:
        file.write(f"api_key={api_key}")

    print(f"API key saved to {file}")

if __name__ == '__main__':
    main()

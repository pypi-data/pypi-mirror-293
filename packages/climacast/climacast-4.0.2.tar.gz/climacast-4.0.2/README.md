# ClimaCast

**ClimaCast** is a command-line weather application that provides real-time weather information for your location or any city of your choice. It has been recently rewritten in Python, offering a more visually appealing and customizable terminal interface using powerful TUI libraries.

## Announcement

### Migration to Python

ClimaCast has been completely rewritten in Python! The original Java version has now been deprecated. This transition allows for enhanced aesthetics and a more engaging user experience through the use of Python's rich Text User Interface (TUI) libraries.

### Why the Change?

While the Java version served well, Python offers a range of beautiful TUI libraries that make it possible to display weather data in a more visually appealing manner. This rewrite focuses on maintaining the original functionality of ClimaCast while laying the groundwork for a more interactive and polished interface.

## Features

- **Real-Time Weather:** Get current weather conditions based on your IP address or a city name you provide.
- **Detailed Weather Data:** Includes temperature, feels like, weather condition, humidity, wind speed, sunrise/sunset times, atmospheric pressure, and visibility.
- **Interactive TUI (Coming Soon):** A more engaging and visually appealing terminal interface powered by Python's TUI libraries.

## Installation

### From PyPI

You can easily install ClimaCast using pip:

```bash
pip install climacast
```

## Usage

To run climacast, simply run the following command

```bash
climacast 
```

By default, ClimaCast will detect your location automatically. You can also specify a city name as a command-line argument:

```bash
climacast Kolkata
```

## Contributing

Contributions are welcome! Feel free to submit a pull request or open an issue to discuss any changes or improvements.

## License

This project is licensed under the GNU General Public License v3.0. See the LICENSE file for more details.
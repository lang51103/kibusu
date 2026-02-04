
# Simple Node.js Weather App

A minimal Express app that fetches current weather for a city using the OpenWeatherMap API and displays it in a small EJS view.

## Features
- Enter a city name and receive current temperature in Fahrenheit.
- Lightweight single-file server with an EJS view and simple CSS.

## Prerequisites
- Node.js (v10+ recommended)
- An OpenWeatherMap API key: https://openweathermap.org/api

## Install

1. Install dependencies:

```
npm install
```

2. Provide your OpenWeatherMap API key by editing `server.js` and replacing the `apiKey` value near the top of the file:

```js
const apiKey = 'YOUR_OPENWEATHERMAP_API_KEY';
```

(Optional) You can modify the app to read the key from an environment variable instead.

## Run

Start the app:

```
npm start
```

Open your browser at http://localhost:3000 and enter a city name.

## Project structure
- `server.js` - Express server and OpenWeatherMap request logic.
- `views/index.ejs` - Simple form and output template.
- `public/css/style.css` - Basic styling for the page.
- `package.json` - Project metadata and scripts.

## Dependencies
- express
- body-parser
- request

These are defined in `package.json` and installed with `npm install`.

## Troubleshooting
- If you see "Error, please try again", ensure your API key is valid and the city name is correct.
- If the server won't start, check for port conflicts on port 3000.

## License
ISC

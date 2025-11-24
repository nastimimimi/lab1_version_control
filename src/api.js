// src/api.js
const axios = require('axios');

async function getJoke() {
    const res = await axios.get("https://api.chucknorris.io/jokes/random");
    return res.data;
}

module.exports = getJoke;

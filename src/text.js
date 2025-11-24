// src/text.js

function toUpper(text) {
    return text.toUpperCase();
}

function reverse(text) {
    return text.split('').reverse().join('');
}

function countWords(text) {
    return text.trim().split(/\s+/).length;
}

module.exports = { toUpper, reverse, countWords };

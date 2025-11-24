// src/user.js

function createUser(name, age) {
    return { name, age, active: true };
}

function deactivateUser(user) {
    user.active = false;
    return user;
}

module.exports = { createUser, deactivateUser };

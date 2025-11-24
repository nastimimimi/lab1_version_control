// tests/user.test.js
const { createUser, deactivateUser } = require('../src/user');

test("Створення нового користувача", () => {
    const u = createUser("Nastia", 18);
    expect(u.name).toBe("Nastia");
    expect(u.active).toBe(true);
});

test("Деактивація користувача", () => {
    const user = createUser("Mark", 25);
    const updated = deactivateUser(user);
    expect(updated.active).toBe(false);
});

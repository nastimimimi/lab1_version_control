// tests/text.test.js
const { toUpper, reverse, countWords } = require('../src/text');

test("Переводить текст у верхній регістр", () => {
    expect(toUpper("hello")).toBe("HELLO");
});

test("Перевертає рядок", () => {
    expect(reverse("cat")).toBe("tac");
});

test("Рахує кількість слів", () => {
    expect(countWords("I love cats")).toBe(3);
});

// tests/api.test.js
const getJoke = require('../src/api');
const axios = require('axios');

jest.mock('axios');

test("Отримує жарт з API", async () => {
    axios.get.mockResolvedValue({
        data: { id: "123", value: "Funny joke!" }
    });

    const result = await getJoke();
    expect(result.value).toBe("Funny joke!");
});

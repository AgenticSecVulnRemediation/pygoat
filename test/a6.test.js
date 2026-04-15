/**
 * Assumptions:
 * - Jest test environment is jsdom.
 * - This test focuses on the changed behavior: event5 sanitizes the submitted code using DOMPurify.
 */

describe("introduction/static/js/a6.js", () => {
  beforeEach(() => {
    jest.resetModules();
    document.body.innerHTML = `<textarea id="a6_t1"></textarea>`;

    global.Headers = function () {
      return {};
    };
    global.FormData = function () {
      const store = new Map();
      return {
        append: (k, v) => store.set(k, v),
        _get: (k) => store.get(k),
      };
    };

    global.DOMPurify = {
      sanitize: jest.fn((v) => `SANITIZED(${v})`),
    };

    global.fetch = jest.fn(() =>
      Promise.resolve({
        text: () => Promise.resolve(JSON.stringify({ message: "success" })),
      })
    );

    global.alert = jest.fn();
  });

  test("event5 sanitizes code before POSTing", async () => {
    // Arrange
    document.getElementById("a6_t1").value = "<img src=x onerror=alert(1)>";

    require("../src/introduction/static/js/a6.js"); // defines global event5

    // Act
    global.event5();

    await Promise.resolve();
    await Promise.resolve();

    // Assert
    expect(global.DOMPurify.sanitize).toHaveBeenCalledWith("<img src=x onerror=alert(1)>");

    const [, requestOptions] = global.fetch.mock.calls[0];
    expect(requestOptions.method).toBe("POST");
    expect(requestOptions.body._get("code")).toBe("SANITIZED(<img src=x onerror=alert(1)>)");
  });
});

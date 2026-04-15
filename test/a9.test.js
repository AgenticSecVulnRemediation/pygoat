/**
 * Assumptions:
 * - Jest test environment is jsdom.
 * - This test focuses on the changed behavior: user inputs are passed through DOMPurify.sanitize before being sent.
 */

describe("introduction/static/js/a9.js", () => {
  beforeEach(() => {
    jest.resetModules();
    document.body.innerHTML = `
      <textarea id="a9_log"></textarea>
      <textarea id="a9_api"></textarea>
      <div id="a9_d3"></div>
    `;

    global.Headers = function () {
      return { append: jest.fn() };
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
        text: () => Promise.resolve(JSON.stringify({ logs: [] })),
      })
    );
  });

  test("event3 sanitizes log_code and api_code before sending", async () => {
    // Arrange
    document.getElementById("a9_log").value = "<img src=x onerror=alert(1)>";
    document.getElementById("a9_api").value = "<svg/onload=alert(2)>";

    require("../src/introduction/static/js/a9.js"); // defines global event3

    // Act
    global.event3();

    // Allow promise chain to run
    await Promise.resolve();
    await Promise.resolve();

    // Assert
    expect(global.DOMPurify.sanitize).toHaveBeenCalledWith("<img src=x onerror=alert(1)>");
    expect(global.DOMPurify.sanitize).toHaveBeenCalledWith("<svg/onload=alert(2)>");

    const [, requestOptions] = global.fetch.mock.calls[0];
    expect(requestOptions.method).toBe("POST");

    // Ensure sanitized values were appended to the request FormData
    expect(requestOptions.body._get("log_code")).toBe("SANITIZED(<img src=x onerror=alert(1)>)");
    expect(requestOptions.body._get("api_code")).toBe("SANITIZED(<svg/onload=alert(2)>)");
  });
});

/**
 * Assumptions:
 * - Jest test environment uses JSDOM.
 * - a9.js defines global `event3` function.
 */

describe('a9.js - escapes log_code/api_code before sending', () => {
  beforeEach(() => {
    jest.resetModules();
    document.body.innerHTML = `
      <input id="a9_log" value="<img src=x onerror=alert(1)>" />
      <input id="a9_api" value="</script><script>alert(1)</script>" />
      <div id="a9_d3"></div>
    `;

    global.fetch = jest.fn(() =>
      Promise.resolve({
        text: () => Promise.resolve(JSON.stringify({ logs: [] })),
      })
    );
  });

  test('escapes special HTML characters when appending to FormData', async () => {
    // Arrange
    const appendSpy = jest.fn();
    global.FormData = function FormDataMock() {
      this.append = appendSpy;
    };

    // Act
    require('../introduction/static/js/a9.js');
    await global.event3();

    // Assert (only verify the delta behavior: escaping inputs before sending)
    const logAppend = appendSpy.mock.calls.find((c) => c[0] === 'log_code');
    const apiAppend = appendSpy.mock.calls.find((c) => c[0] === 'api_code');

    expect(logAppend[1]).toBe('&lt;img src=x onerror=alert(1)&gt;');
    expect(apiAppend[1]).toBe('&lt;/script&gt;&lt;script&gt;alert(1)&lt;/script&gt;');
  });
});

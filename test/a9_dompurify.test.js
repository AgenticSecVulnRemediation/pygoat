// Note: this test stubs DOMPurify to avoid requiring the real dependency in unit tests.

describe('a9.js uses DOMPurify.sanitize for outgoing form fields', () => {
  test('event3 calls DOMPurify.sanitize for both inputs and sends sanitized values', () => {
    // Arrange
    document.body.innerHTML = `
      <input id="a9_log" value="<b>LOG</b>" />
      <input id="a9_api" value="<img>" />
      <div id="a9_d3" style="display:none"></div>
    `;

    const appendCalls = [];
    global.FormData = function () {
      this.append = (k, v) => appendCalls.push([k, v]);
    };

    // Provide a DOMPurify stub compatible with the module's usage.
    jest.doMock('dompurify', () => ({
      __esModule: true,
      default: {
        sanitize: jest.fn((v) => `SANITIZED:${v}`),
      },
    }));

    global.fetch = jest.fn().mockResolvedValue({
      text: () => Promise.resolve(JSON.stringify({ logs: [] }))
    });

    jest.isolateModules(() => {
      require('../introduction/static/js/a9.js');
    });

    // Act
    global.event3();

    // Assert
    const logAppend = appendCalls.find(([k]) => k === 'log_code');
    const apiAppend = appendCalls.find(([k]) => k === 'api_code');

    expect(logAppend[1]).toBe('SANITIZED:<b>LOG</b>');
    expect(apiAppend[1]).toBe('SANITIZED:<img>');
  });
});

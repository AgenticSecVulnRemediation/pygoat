const path = require('path');

describe('ssrf.js sanitize() usage', () => {
  beforeEach(() => {
    jest.resetModules();
  });

  test('checkcode sanitizes both python and html values before appending to FormData', async () => {
    // Arrange
    const pythonEl = { value: "<img src=x onerror=alert(1)>" };
    const htmlEl = { value: "a/b&<>'\"" };

    global.document = {
      getElementById: jest.fn((id) => {
        if (id === 'python') return pythonEl;
        if (id === 'html') return htmlEl;
        if (id.startsWith('ssrf-frame-') || id.startsWith('ssrf-bar-status')) return { style: {}, classList: { add: jest.fn() } };
        throw new Error(`unexpected id ${id}`);
      }),
      querySelectorAll: jest.fn(() => []),
    };

    const appendMock = jest.fn();
    global.FormData = function FormData() {
      this.append = appendMock;
    };

    global.fetch = jest.fn(() => Promise.resolve({ text: () => Promise.resolve(JSON.stringify({ passed: 0, message: 'ok' })) }));
    global.alert = jest.fn();

    // Act
    require(path.resolve(process.cwd(), 'introduction/static/Lab/ssrf.js'));
    await global.checkcode();

    // Assert
    expect(appendMock).toHaveBeenCalledWith('python_code', '&lt;img src=x onerror=alert(1)&gt;');
    expect(appendMock).toHaveBeenCalledWith('html_code', 'a&#x2F;b&amp;&lt;&gt;&#x27;&quot;');
  });
});

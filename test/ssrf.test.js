// Note: source file is under introduction/static/Lab/ssrf.js; assume Jest is configured with jsdom.

describe('ssrf.js checkcode sanitization', () => {
  beforeEach(() => {
    jest.resetModules();
    document.body.innerHTML = `
      <textarea id="python"></textarea>
      <textarea id="html"></textarea>
    `;

    global.fetch = jest.fn(() => Promise.resolve({
      text: () => Promise.resolve(JSON.stringify({ message: 'ok', passed: 0 }))
    }));

    global.FormData = class {
      constructor() { this._data = {}; }
      append(k, v) { this._data[k] = v; }
    };

    jest.spyOn(window, 'alert').mockImplementation(() => {});
  });

  test('checkcode escapes HTML special characters before sending to backend', async () => {
    // Arrange
    require('../introduction/static/Lab/ssrf.js');

    document.getElementById('python').value = 'print(1)';
    document.getElementById('html').value = `<img src=x onerror=alert('x')>&"'`;

    // Act
    await global.checkcode();

    // Assert
    const fd = global.fetch.mock.calls[0][1].body;
    expect(fd._data.python_code).toBe('print(1)');
    expect(fd._data.html_code).toBe('&lt;img src=x onerror=alert(&#39;x&#39;)&gt;&amp;&quot;&#39;');
  });
});

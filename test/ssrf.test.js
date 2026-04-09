// NOTE: This repo has multiple PRs touching introduction/static/Lab/ssrf.js.
// It is intentional that different PRs may each add a test file with the same path (test/ssrf.test.js)
// because they land on different branches/PRs.

describe('ssrf.js sanitize() escapes special characters', () => {
  test('checkcode sanitizes both python_code and html_code', () => {
    // Arrange
    document.body.innerHTML = `
      <textarea id="python">&<>'"/</textarea>
      <textarea id="html">&<>'"/</textarea>
    `;

    const appendCalls = [];
    global.FormData = function () {
      this.append = (k, v) => appendCalls.push([k, v]);
    };

    global.fetch = jest.fn().mockResolvedValue({ text: () => Promise.resolve('{"passed":0,"message":"no"}') });

    jest.isolateModules(() => {
      require('../introduction/static/Lab/ssrf.js');
    });

    // Act
    global.checkcode();

    // Assert
    const pythonAppend = appendCalls.find(([k]) => k === 'python_code');
    const htmlAppend = appendCalls.find(([k]) => k === 'html_code');

    expect(pythonAppend[1]).toBe('&amp;&lt;&gt;&#39;&quot;&#x2F;');
    expect(htmlAppend[1]).toBe('&amp;&lt;&gt;&#39;&quot;&#x2F;');
  });
});

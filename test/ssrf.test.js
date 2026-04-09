describe('ssrf.js sanitizeHTML', () => {
  test('escapes HTML special characters before sending', () => {
    // Arrange
    document.body.innerHTML = `
      <textarea id="python">print('hi')</textarea>
      <textarea id="html"><img src=x onerror=alert(1)></textarea>
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
    const htmlAppend = appendCalls.find(([k]) => k === 'html_code');
    expect(htmlAppend).toBeDefined();
    expect(htmlAppend[1]).toBe('&lt;img src=x onerror=alert(1)&gt;');
  });
});

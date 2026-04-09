describe('a6.js sanitizeInput', () => {
  test('event5 sends sanitized code (escapes < and >)', () => {
    // Arrange
    document.body.innerHTML = `<textarea id="a6_t1"><img></textarea>`;

    const appendCalls = [];
    global.FormData = function () {
      this.append = (k, v) => appendCalls.push([k, v]);
    };

    global.fetch = jest.fn().mockResolvedValue({ text: () => Promise.resolve('{"message":"success"}') });

    jest.isolateModules(() => {
      require('../introduction/static/js/a6.js');
    });

    // Act
    global.event5();

    // Assert
    const codeAppend = appendCalls.find(([k]) => k === 'code');
    expect(codeAppend[1]).toBe('&lt;img&gt;');
  });
});

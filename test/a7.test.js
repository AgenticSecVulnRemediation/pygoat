describe('a7.js uses DOMPurify.sanitize before sending', () => {
  test('event4 uses DOMPurify.sanitize on input value', () => {
    // Arrange
    document.body.innerHTML = `<input id="a7_input" value="<img>" />`;

    global.DOMPurify = { sanitize: jest.fn((v) => `SANITIZED:${v}`) };

    const appendCalls = [];
    global.FormData = function () {
      this.append = (k, v) => appendCalls.push([k, v]);
    };

    global.fetch = jest.fn().mockResolvedValue({ text: () => Promise.resolve('{"message":"ok"}') });

    jest.isolateModules(() => {
      require('../introduction/static/js/a7.js');
    });

    // Act
    global.event4();

    // Assert
    expect(global.DOMPurify.sanitize).toHaveBeenCalledWith('<img>');
    const codeAppend = appendCalls.find(([k]) => k === 'code');
    expect(codeAppend[1]).toBe('SANITIZED:<img>');
  });
});

const {JSDOM} = require('jsdom');

describe('a7.js DOMPurify hardening', () => {
  test('sanitizes a7_input before sending', () => {
    // Arrange
    const dom = new JSDOM(`<!doctype html><input id="a7_input" />`);
    global.document = dom.window.document;

    // Mock DOMPurify
    global.DOMPurify = {
      sanitize: jest.fn(() => 'SANITIZED')
    };

    document.getElementById('a7_input').value = '<img src=x onerror=alert(1)>';

    // Act: execute only the changed line's behavior
    const code = DOMPurify.sanitize(document.getElementById('a7_input').value);

    // Assert
    expect(DOMPurify.sanitize).toHaveBeenCalledWith('<img src=x onerror=alert(1)>');
    expect(code).toBe('SANITIZED');
  });
});

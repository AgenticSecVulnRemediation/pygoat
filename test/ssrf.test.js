/**
 * @jest-environment jsdom
 */

const path = require('path');

// Importing the module relies on jest/jsdom environment.
require('../../introduction/static/Lab/ssrf.js');


describe('ssrf.js sanitize()', () => {
  test('checkcode sends escaped python_code and html_code to FormData', async () => {
    // Arrange
    document.body.innerHTML = `
      <textarea id="python"></textarea>
      <textarea id="html"></textarea>
    `;

    document.getElementById('python').value = `<script>alert(1)</script> & "'`;
    document.getElementById('html').value = `<img src=x onerror=alert(1)>`;

    const appendSpy = jest.fn();
    global.FormData = function() { this.append = appendSpy; };

    global.fetch = jest.fn().mockResolvedValue({
      text: () => Promise.resolve(JSON.stringify({ message: 'ok', passed: 0 }))
    });

    // Act
    await global.checkcode();

    // Assert
    // both fields must be sanitized before appending
    expect(appendSpy).toHaveBeenCalledWith(
      'python_code',
      expect.not.stringContaining('<')
    );
    expect(appendSpy).toHaveBeenCalledWith(
      'html_code',
      expect.not.stringContaining('<')
    );
    // ensure ampersand escaped too
    const pythonArg = appendSpy.mock.calls.find(c => c[0] === 'python_code')[1];
    expect(pythonArg).toContain('&amp;');
  });
});

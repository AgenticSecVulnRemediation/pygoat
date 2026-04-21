// Jest tests for a7.js DOMPurify hardening

jest.mock('dompurify', () => ({
  sanitize: jest.fn((s) => `SANITIZED:${s}`),
}), { virtual: true });

const DOMPurify = require('dompurify');
const path = require('path');

require(path.resolve(__dirname, '../introduction/static/js/a7.js'));

describe('a7.js hardening (DOMPurify.sanitize for event4)', () => {
  beforeEach(() => {
    document.body.innerHTML = `<input id="a7_input" value=""><div id="a7_d4"></div>`;
  });

  test('event4 sanitizes user input before sending in FormData', async () => {
    // Arrange
    document.getElementById('a7_input').value = '<img src=x onerror=alert(1)>';

    const appendSpy = jest.fn();
    global.FormData = function FormData() { this.append = appendSpy; };
    global.Headers = function Headers() {};

    global.fetch = jest.fn(() => Promise.resolve({
      text: () => Promise.resolve(JSON.stringify({ message: 'ok' }))
    }));

    // Act
    await global.event4();

    // Assert
    expect(DOMPurify.sanitize).toHaveBeenCalledWith('<img src=x onerror=alert(1)>');
    expect(appendSpy).toHaveBeenCalledWith('code', 'SANITIZED:<img src=x onerror=alert(1)>');
  });
});

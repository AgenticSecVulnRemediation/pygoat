/**
 * @jest-environment jsdom
 */

jest.mock('../../introduction/static/js/path/to/dompurify.js', () => ({
  __esModule: true,
  default: { sanitize: jest.fn((x) => `sanitized:${x}`) },
}));

const DOMPurify = require('../../introduction/static/js/path/to/dompurify.js').default;

require('../../introduction/static/js/a7.js');

describe('a7.js event4', () => {
  test('sanitizes input before appending to formdata', () => {
    // Arrange
    document.body.innerHTML = `
      <input id="a7_input" />
      <div id="a7_d4"></div>
    `;
    document.getElementById('a7_input').value = '<img src=x onerror=alert(1)>';

    const appendSpy = jest.fn();
    global.FormData = function () { this.append = appendSpy; };

    global.fetch = jest.fn().mockResolvedValue({
      text: () => Promise.resolve(JSON.stringify({ message: 'ok' }))
    });

    // Act
    global.event4();

    // Assert
    expect(DOMPurify.sanitize).toHaveBeenCalledWith('<img src=x onerror=alert(1)>');
    expect(appendSpy).toHaveBeenCalledWith('code', 'sanitized:<img src=x onerror=alert(1)>');
  });
});

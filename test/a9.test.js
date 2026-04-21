/**
 * @jest-environment jsdom
 */

jest.mock('dompurify', () => ({
  __esModule: true,
  default: { sanitize: jest.fn((x) => `sanitized:${x}`) },
}));

const DOMPurify = require('dompurify').default;

require('../../introduction/static/js/a9.js');

describe('a9.js event3 (DOMPurify sanitize)', () => {
  test('sanitizes log_code and api_code before adding to FormData', () => {
    // Arrange
    document.body.innerHTML = `
      <textarea id="a9_log"></textarea>
      <textarea id="a9_api"></textarea>
      <div id="a9_d3"></div>
      <button id="a9_b1"></button>
      <button id="a9_b2"></button>
      <div id="a9_d1"></div>
      <div id="a9_d2"></div>
    `;
    document.getElementById('a9_log').value = '<img src=x onerror=alert(1)>';
    document.getElementById('a9_api').value = '<svg/onload=alert(2)>';

    const appendSpy = jest.fn();
    global.FormData = function () { this.append = appendSpy; };

    global.fetch = jest.fn().mockResolvedValue({
      text: () => Promise.resolve(JSON.stringify({ logs: [] }))
    });

    // Act
    global.event3();

    // Assert
    expect(DOMPurify.sanitize).toHaveBeenCalledWith('<img src=x onerror=alert(1)>');
    expect(DOMPurify.sanitize).toHaveBeenCalledWith('<svg/onload=alert(2)>');

    expect(appendSpy).toHaveBeenCalledWith('log_code', 'sanitized:<img src=x onerror=alert(1)>');
    expect(appendSpy).toHaveBeenCalledWith('api_code', 'sanitized:<svg/onload=alert(2)>');
  });
});

const path = require('path');

require(path.resolve(__dirname, '../introduction/static/Lab/ssrf.js'));

describe('SSRF lab checkcode DOM XSS mitigation', () => {
  beforeEach(() => {
    document.body.innerHTML = `
      <textarea id="python"></textarea>
      <textarea id="html"></textarea>
      <div id="ssrf-message"></div>
      <div id="ssrf-frame-4"></div>
      <div id="ssrf-frame-5"></div>
      <div id="ssrf-bar-status3"></div>
    `;

    // Provide minimal classList API
    document.getElementById('ssrf-bar-status3').classList = { add: jest.fn() };

    global.fetch = jest.fn(() =>
      Promise.resolve({
        text: () => Promise.resolve(JSON.stringify({ message: '<img src=x onerror=1>', passed: 0 })),
      })
    );

    global.alert = jest.fn();
  });

  test('renders message using textContent when ssrf-message element exists', async () => {
    // Act
    await global.checkcode();

    // Assert: should not alert, and should not interpret HTML
    expect(global.alert).not.toHaveBeenCalled();
    expect(document.getElementById('ssrf-message').textContent).toBe('<img src=x onerror=1>');
    expect(document.getElementById('ssrf-message').innerHTML).toBe('&lt;img src=x onerror=1&gt;');
  });

  test('falls back to alert when ssrf-message element is missing', async () => {
    // Arrange
    document.getElementById('ssrf-message').remove();

    // Act
    await global.checkcode();

    // Assert
    expect(global.alert).toHaveBeenCalledWith('<img src=x onerror=1>');
  });
});

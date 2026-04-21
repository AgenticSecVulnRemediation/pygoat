// Jest tests for a9.js (render logs safely)
// Assumption: Jest runs in jsdom.

const path = require('path');

require(path.resolve(__dirname, '../introduction/static/js/a9.js'));

describe('a9.js XSS hardening (textContent for logs)', () => {
  beforeEach(() => {
    document.body.innerHTML = `
      <input id="a9_log" value="log">
      <input id="a9_api" value="api">
      <ul id="a9_d3"></ul>
    `;
  });

  test('event3 uses textContent so payload is not interpreted as HTML', async () => {
    // Arrange
    const payload = '<img src=x onerror=alert(1)>';

    global.Headers = function Headers() { this.append = jest.fn(); };
    global.FormData = function FormData() { this.append = jest.fn(); };

    global.fetch = jest.fn(() => Promise.resolve({
      text: () => Promise.resolve(JSON.stringify({ logs: [payload] }))
    }));

    // Act
    await global.event3();

    // Assert
    const list = document.getElementById('a9_d3');
    expect(list.querySelectorAll('li')).toHaveLength(1);
    expect(list.innerHTML).not.toContain('<img');
    expect(list.textContent).toContain(payload);
  });
});

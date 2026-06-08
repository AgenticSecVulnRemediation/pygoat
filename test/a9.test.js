/**
 * Assumptions:
 * - Jest is configured for this repo.
 * - This test focuses only on the security fix: using textContent instead of innerHTML.
 */

describe('a9.js event3 XSS hardening', () => {
  beforeEach(() => {
    document.body.innerHTML = `
      <input id="a9_log" value="log" />
      <input id="a9_api" value="api" />
      <div id="a9_d3"></div>
    `;

    // Minimal stubs used by event3
    global.Headers = function Headers() {
      this.append = jest.fn();
    };
    global.FormData = function FormData() {
      this.append = jest.fn();
    };
  });

  afterEach(() => {
    jest.resetModules();
    delete global.fetch;
  });

  test('event3 renders logs via textContent (does not interpret HTML)', async () => {
    // Arrange: malicious-looking string that would become HTML if innerHTML were used.
    const payload = '<img src=x onerror="window.__XSS__=true">hello';

    global.fetch = jest.fn().mockResolvedValue({
      text: () => Promise.resolve(JSON.stringify({ logs: [payload] })),
    });

    // Load the script (defines global event3)
    require('../introduction/static/js/a9.js');

    // Act
    await global.event3();

    // Assert
    const out = document.getElementById('a9_d3');
    const li = out.querySelector('li');
    expect(li).not.toBeNull();

    // Key security assertion: no HTML interpreted/inserted
    expect(li.innerHTML).toBe(payload); // innerHTML reflects text when set via textContent
    expect(li.querySelector('img')).toBeNull();
  });
});

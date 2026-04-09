/**
 * Assumptions:
 * - Jest test environment uses JSDOM.
 * - Source file is loaded as a side-effect module.
 */

describe('a9.js XSS fix: uses textContent instead of innerHTML', () => {
  beforeEach(() => {
    document.body.innerHTML = `
      <input id="a9_log" value="log" />
      <input id="a9_api" value="api" />
      <div id="a9_d3"></div>
    `;

    global.fetch = jest.fn(() =>
      Promise.resolve({
        text: () => Promise.resolve(JSON.stringify({ logs: ['<img src=x onerror=alert(1)>'] })),
      })
    );

    // Minimal stubs used by the script
    global.Headers = function Headers() {
      this.append = jest.fn();
    };
    global.FormData = function FormData() {
      this.append = jest.fn();
    };

    jest.resetModules();
    require('../introduction/static/js/a9.js');
  });

  afterEach(() => {
    jest.restoreAllMocks();
    delete global.fetch;
    delete global.Headers;
    delete global.FormData;
  });

  test('event3 appends log entries as text nodes (no HTML interpretation)', async () => {
    // Arrange
    const container = document.getElementById('a9_d3');

    // Act
    await global.event3();

    // Allow promise chain to complete
    await new Promise(setImmediate);

    // Assert
    const li = container.querySelector('li');
    expect(li).not.toBeNull();
    expect(li.textContent).toBe('<img src=x onerror=alert(1)>');
    expect(li.innerHTML).toBe('&lt;img src=x onerror=alert(1)&gt;');
  });
});

/**
 * Assumptions:
 * - This test runs in Jest with JSDOM environment.
 * - The source file is available at: introduction/static/js/a7.js
 */

describe('a7.js event4 sanitization', () => {
  beforeEach(() => {
    document.body.innerHTML = `
      <input id="a7_input" />
      <div id="a7_d4"></div>
    `;

    global.fetch = jest.fn(() =>
      Promise.resolve({
        text: () => Promise.resolve(JSON.stringify({ message: 'ok' })),
      })
    );
  });

  afterEach(() => {
    jest.resetModules();
    jest.clearAllMocks();
    delete global.fetch;
  });

  test('event4 escapes HTML special characters before sending in FormData', async () => {
    // Arrange
    const payload = `<img src=x onerror=alert(1)>`;
    document.getElementById('a7_input').value = payload;

    // Spy on FormData.append to capture the value being sent.
    const appendSpy = jest.spyOn(FormData.prototype, 'append');

    // Act
    require('../introduction/static/js/a7.js');
    await global.event4();

    // Assert
    const codeAppend = appendSpy.mock.calls.find((c) => c[0] === 'code');
    expect(codeAppend).toBeTruthy();

    const sentValue = codeAppend[1];
    expect(sentValue).toContain('&lt;img');
    expect(sentValue).toContain('onerror=alert(1)');
    expect(sentValue).toContain('&gt;');
    expect(sentValue).not.toContain('<img');
  });
});

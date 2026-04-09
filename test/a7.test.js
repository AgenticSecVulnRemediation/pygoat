/**
 * Assumptions:
 * - Jest test environment uses JSDOM.
 * - Source file is loaded as a side-effect module.
 */

describe('a7.js escapes HTML special characters before sending', () => {
  beforeEach(() => {
    document.body.innerHTML = `
      <input id="a7_input" />
      <div id="a7_d4"></div>
    `;

    document.getElementById('a7_input').value = `<img src=x onerror="alert('x')">`;

    global.fetch = jest.fn(() =>
      Promise.resolve({
        text: () => Promise.resolve(JSON.stringify({ message: 'ok' })),
      })
    );

    global.Headers = function Headers() {};
    global.FormData = function FormData() {
      this.append = jest.fn();
    };

    jest.resetModules();
    require('../introduction/static/js/a7.js');
  });

  afterEach(() => {
    jest.restoreAllMocks();
    delete global.fetch;
    delete global.Headers;
    delete global.FormData;
  });

  test('event4 appends escaped code (no raw < or >)', async () => {
    // Act
    global.event4();
    await new Promise(setImmediate);

    // Assert
    const formDataInstance = global.FormData.mock.instances[0];
    const codeAppendCall = formDataInstance.append.mock.calls.find((c) => c[0] === 'code');
    expect(codeAppendCall).toBeDefined();
    const escaped = codeAppendCall[1];
    expect(escaped).toContain('&lt;img');
    expect(escaped).toContain('&gt;');
    expect(escaped).not.toContain('<img');
  });
});

/**
 * Assumptions:
 * - Jest test environment uses JSDOM.
 * - Source file is loaded as a side-effect module.
 */

describe('ssrf.js escapes HTML before sending html_code', () => {
  beforeEach(() => {
    document.body.innerHTML = `
      <textarea id="python"></textarea>
      <textarea id="html"></textarea>
    `;

    document.getElementById('python').value = 'print(1)';
    document.getElementById('html').value = `<img src=x onerror="alert('x')">`;

    global.fetch = jest.fn(() =>
      Promise.resolve({
        text: () => Promise.resolve(JSON.stringify({ message: 'ok', passed: 0 })),
      })
    );

    global.FormData = function FormData() {
      this.append = jest.fn();
    };

    jest.resetModules();
    require('../introduction/static/Lab/ssrf.js');
  });

  afterEach(() => {
    jest.restoreAllMocks();
    delete global.fetch;
    delete global.FormData;
  });

  test('checkcode appends escaped html_code (no raw < or >)', async () => {
    // Act
    global.checkcode();
    await new Promise(setImmediate);

    // Assert
    const formDataInstance = global.FormData.mock.instances[0];
    const htmlAppendCall = formDataInstance.append.mock.calls.find((c) => c[0] === 'html_code');
    expect(htmlAppendCall).toBeDefined();
    const escaped = htmlAppendCall[1];
    expect(escaped).toContain('&lt;img');
    expect(escaped).toContain('&gt;');
    expect(escaped).not.toContain('<img');
  });
});

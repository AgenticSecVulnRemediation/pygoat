/**
 * Jest unit tests for introduction/static/Lab/ssrf.js
 *
 * Assumption: tests run in jsdom environment (Jest default in many setups).
 * The source file is not a module; this test uses eval() to load functions into the test scope.
 */

const fs = require('fs');
const path = require('path');

function loadSource(relativePath) {
  const abs = path.join(process.cwd(), relativePath);
  const code = fs.readFileSync(abs, 'utf8');
  // eslint-disable-next-line no-eval
  eval(code);
}

describe('ssrf.js checkcode() - DOMPurify sanitization', () => {
  beforeEach(() => {
    // Minimal DOM nodes used by checkcode()
    document.body.innerHTML = `
      <textarea id="python"></textarea>
      <textarea id="html"></textarea>
    `;

    global.DOMPurify = {
      sanitize: jest.fn((v) => `SANITIZED:${v}`),
    };

    global.FormData = class {
      constructor() {
        this._entries = [];
      }
      append(k, v) {
        this._entries.push([k, v]);
      }
      getAll() {
        return this._entries;
      }
    };

    global.fetch = jest.fn(() =>
      Promise.resolve({
        text: () => Promise.resolve('{"passed":0,"message":"ok"}'),
      })
    );

    jest.spyOn(global, 'alert').mockImplementation(() => {});

    loadSource('introduction/static/Lab/ssrf.js');
  });

  afterEach(() => {
    jest.restoreAllMocks();
    delete global.DOMPurify;
  });

  test('sanitizes python and html before appending to FormData', async () => {
    // Arrange
    document.getElementById('python').value = '<img src=x onerror=1>';
    document.getElementById('html').value = '<script>alert(1)</script>';

    // Act
    checkcode();

    // Allow promise chain to flush
    await Promise.resolve();

    // Assert
    expect(global.DOMPurify.sanitize).toHaveBeenCalledWith('<img src=x onerror=1>');
    expect(global.DOMPurify.sanitize).toHaveBeenCalledWith('<script>alert(1)</script>');

    const fetchArgs = global.fetch.mock.calls[0];
    expect(fetchArgs[0]).toBe('api/ssrf');
    const body = fetchArgs[1].body;

    expect(body.getAll()).toEqual([
      ['python_code', 'SANITIZED:<img src=x onerror=1>'],
      ['html_code', 'SANITIZED:<script>alert(1)</script>'],
    ]);
  });
});

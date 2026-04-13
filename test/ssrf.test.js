/**
 * Jest unit tests for introduction/static/Lab/ssrf.js
 *
 * Assumption: tests run in jsdom environment.
 */

const fs = require('fs');
const path = require('path');

function loadSource(relativePath) {
  const abs = path.join(process.cwd(), relativePath);
  const code = fs.readFileSync(abs, 'utf8');
  // eslint-disable-next-line no-eval
  eval(code);
}

describe('ssrf.js checkcode() - escapeHTML before sending html_code', () => {
  beforeEach(() => {
    document.body.innerHTML = `
      <textarea id="python"></textarea>
      <textarea id="html"></textarea>
    `;

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
  });

  test('escapes html before appending to FormData', async () => {
    // Arrange
    document.getElementById('python').value = 'print(1)';
    document.getElementById('html').value = `<img src=x onerror="alert('x')">`;

    // Act
    checkcode();
    await Promise.resolve();

    // Assert
    const body = global.fetch.mock.calls[0][1].body;
    const entries = body.getAll();

    expect(entries[0]).toEqual(['python_code', 'print(1)']);
    expect(entries[1][0]).toBe('html_code');
    expect(entries[1][1]).toContain('&lt;img');
    expect(entries[1][1]).toContain('&quot;');
    expect(entries[1][1]).toContain('&#39;');
  });
});

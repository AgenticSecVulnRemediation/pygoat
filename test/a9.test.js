// Assumptions:
// - Source file is at introduction/static/js/a9.js and is loaded via fs+vm.
// - Delta: rendering logs should use textContent (not innerHTML) to prevent XSS.

const fs = require('fs');
const path = require('path');
const vm = require('vm');

describe('a9.js event3 log rendering hardening', () => {
  beforeEach(() => {
    document.body.innerHTML = `
      <textarea id="a9_log"></textarea>
      <textarea id="a9_api"></textarea>
      <div id="a9_d3"></div>
      <button id="a9_b1"></button>
      <button id="a9_b2"></button>
      <div id="a9_d1"></div>
      <div id="a9_d2"></div>
    `;

    global.Headers = function Headers() {
      this.append = jest.fn();
    };
    global.FormData = function FormData() {
      this._data = {};
      this.append = (k, v) => (this._data[k] = v);
    };

    global.fetch = jest.fn(() => Promise.resolve({
      text: () => Promise.resolve(JSON.stringify({ logs: ['<img src=x onerror=alert(1)>'] }))
    }));

    const code = fs.readFileSync(path.join(process.cwd(), 'introduction/static/js/a9.js'), 'utf8');
    vm.runInThisContext(code);
  });

  test('uses textContent so attacker-controlled logs are not interpreted as HTML', async () => {
    // Arrange
    document.getElementById('a9_log').value = 'x';
    document.getElementById('a9_api').value = 'y';

    // Act
    event3();
    await Promise.resolve();
    await Promise.resolve();

    // Assert
    const li = document.querySelector('#a9_d3 li');
    expect(li).not.toBeNull();
    expect(li.textContent).toBe('<img src=x onerror=alert(1)>');
    expect(li.innerHTML).toBe('&lt;img src=x onerror=alert(1)&gt;');
  });
});

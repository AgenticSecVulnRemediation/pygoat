/**
 * Assumptions:
 * - Jest test environment is jsdom.
 * - a9.js defines global function event3.
 */

describe('introduction/static/js/a9.js - event3 uses textContent instead of innerHTML for logs', () => {
  beforeEach(() => {
    document.body.innerHTML = `
      <input id="a9_log" />
      <input id="a9_api" />
      <div id="a9_d3"></div>
    `;

    global.Headers = function Headers() {
      this.append = jest.fn();
    };

    global.FormData = class FormDataMock {
      constructor() {
        this._data = new Map();
      }
      append(k, v) {
        this._data.set(k, v);
      }
      get(k) {
        return this._data.get(k);
      }
    };

    global.fetch = jest.fn().mockResolvedValue({
      text: () =>
        Promise.resolve(
          JSON.stringify({
            logs: ['<img src=x onerror=alert(1)>'],
          })
        ),
    });
  });

  afterEach(() => {
    jest.resetModules();
    jest.clearAllMocks();
  });

  test('renders potentially dangerous log entry as text (escaped in innerHTML)', async () => {
    // Arrange
    document.getElementById('a9_log').value = 'x';
    document.getElementById('a9_api').value = 'y';

    // Act
    require('../introduction/static/js/a9.js');
    await global.event3();

    // Assert
    const li = document.querySelector('#a9_d3 li');
    expect(li).not.toBeNull();
    expect(li.textContent).toBe('<img src=x onerror=alert(1)>');
    expect(li.innerHTML).toBe('&lt;img src=x onerror=alert(1)&gt;');
  });
});

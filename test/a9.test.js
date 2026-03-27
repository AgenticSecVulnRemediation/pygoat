/**
 * Assumptions:
 * - Jest test environment is jsdom.
 * - a9.js defines global functions event1/event2/event3.
 */

describe('introduction/static/js/a9.js - event3 escapes input and uses textContent for logs', () => {
  beforeEach(() => {
    document.body.innerHTML = `
      <input id="a9_log" />
      <input id="a9_api" />
      <div id="a9_d3"></div>
      <button id="a9_b1"></button>
      <div id="a9_d1"></div>
      <button id="a9_b2"></button>
      <div id="a9_d2"></div>
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
            logs: ['<b>unsafe</b>'],
          })
        ),
    });
  });

  afterEach(() => {
    jest.resetModules();
    jest.clearAllMocks();
  });

  test('escapes log_code/api_code and renders logs via textContent (no HTML injection)', async () => {
    // Arrange
    document.getElementById('a9_log').value = `<img src=x onerror=alert(1)>`;
    document.getElementById('a9_api').value = `<script>alert(1)</script>`;

    // Act
    require('../introduction/static/js/a9.js');
    await global.event3();

    // Assert: request payload is escaped
    const [, requestOptions] = global.fetch.mock.calls[0];
    expect(requestOptions.body.get('log_code')).toBe('&lt;img src=x onerror=alert(1)&gt;');
    expect(requestOptions.body.get('api_code')).toBe('&lt;script&gt;alert(1)&lt;/script&gt;');

    // Assert: rendered list item uses textContent (innerHTML should remain empty)
    const li = document.querySelector('#a9_d3 li');
    expect(li).not.toBeNull();
    expect(li.textContent).toBe('<b>unsafe</b>');
    expect(li.innerHTML).toBe('&lt;b&gt;unsafe&lt;/b&gt;');
  });
});

/**
 * @jest-environment jsdom
 */

describe('a9.js sanitizeInput', () => {
  beforeEach(() => {
    document.body.innerHTML = `
      <input id="a9_log" value="<script>alert(1)</script>" />
      <input id="a9_api" value="<b>hi</b>" />
      <ul id="a9_d3"></ul>
    `;

    jest.resetModules();
  });

  test('sanitizes fields before putting them into FormData', async () => {
    const fetchSpy = jest.fn(() =>
      Promise.resolve({
        text: () => Promise.resolve(JSON.stringify({ logs: [] })),
      })
    );
    global.fetch = fetchSpy;

    const fields = {};
    global.FormData = class {
      append(k, v) {
        fields[k] = v;
      }
    };

    require('../../introduction/static/js/a9.js');

    await global.event3();

    expect(fields.log_code).toContain('&lt;script&gt;');
    expect(fields.log_code).not.toContain('<script>');
    expect(fields.api_code).toContain('&lt;b&gt;');
    expect(fields.api_code).not.toContain('<b>');
  });
});

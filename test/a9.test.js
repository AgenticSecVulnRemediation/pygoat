/**
 * Assumptions:
 * - Jest test environment uses JSDOM.
 * - a9.js defines global `sanitize` and `event3`.
 */

describe('a9.js - sanitizes log_code/api_code before sending', () => {
  beforeEach(() => {
    jest.resetModules();
    document.body.innerHTML = `
      <input id="a9_log" value="<b>bold</b>" />
      <input id="a9_api" value="&" />
      <div id="a9_d3"></div>
    `;

    global.fetch = jest.fn(() =>
      Promise.resolve({
        text: () => Promise.resolve(JSON.stringify({ logs: [] })),
      })
    );
  });

  test('sanitizes before appending to FormData', async () => {
    const appendSpy = jest.fn();
    global.FormData = function FormDataMock() {
      this.append = appendSpy;
    };

    require('../introduction/static/js/a9.js');
    await global.event3();

    const logAppend = appendSpy.mock.calls.find((c) => c[0] === 'log_code');
    const apiAppend = appendSpy.mock.calls.find((c) => c[0] === 'api_code');

    expect(logAppend[1]).toBe('&lt;b&gt;bold&lt;/b&gt;');
    expect(apiAppend[1]).toBe('&amp;');
  });
});

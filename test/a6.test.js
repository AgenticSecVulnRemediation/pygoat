const path = require('path');

require(path.resolve(__dirname, '../introduction/static/js/a6.js'));

describe('A6 discussion event5/event6 escapeHtml', () => {
  beforeEach(() => {
    document.body.innerHTML = `
      <textarea id="a6_t1"></textarea>
      <div id="a6_d5"></div>
    `;

    global.fetch = jest.fn(() =>
      Promise.resolve({
        text: () => Promise.resolve(JSON.stringify({ message: 'success', vulns: [] })),
      })
    );

    global.alert = jest.fn();
  });

  test('event5 sends escaped code in FormData', async () => {
    document.getElementById('a6_t1').value = `<img src=x onerror=1>`;

    const appended = {};
    global.FormData = class {
      append(k, v) {
        appended[k] = v;
      }
    };

    await global.event5();

    expect(appended.code).toBe('&lt;img src=x onerror=1&gt;');
    expect(global.fetch).toHaveBeenCalledTimes(1);
  });

  test('event6 sends escaped code in FormData', async () => {
    document.getElementById('a6_t1').value = `a&b"c'd`;

    const appended = {};
    global.FormData = class {
      append(k, v) {
        appended[k] = v;
      }
    };

    await global.event6();

    expect(appended.code).toBe('a&amp;b&quot;c&#39;d');
    expect(global.fetch).toHaveBeenCalledTimes(1);
  });
});

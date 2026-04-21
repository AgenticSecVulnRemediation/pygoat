/**
 * @jest-environment jsdom
 */

describe('a9.js event3 log rendering', () => {
  beforeEach(() => {
    document.body.innerHTML = `
      <input id="a9_log" value="" />
      <input id="a9_api" value="" />
      <ul id="a9_d3" style="display:none"></ul>
    `;

    jest.resetModules();
  });

  test('appends logs using textContent (prevents DOM XSS)', async () => {
    const malicious = '<img src=x onerror="window.__xss = true">X';

    global.fetch = jest.fn(() =>
      Promise.resolve({
        text: () => Promise.resolve(JSON.stringify({ logs: [malicious] })),
      })
    );

    require('../../introduction/static/js/a9.js');

    await global.event3();

    const li = document.querySelector('#a9_d3 li');
    expect(li).not.toBeNull();
    expect(li.querySelector('img')).toBeNull();
    expect(li.textContent).toBe(malicious);
  });
});

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

    // Load the script under test into the JSDOM environment.
    jest.resetModules();
  });

  test('uses textContent (not innerHTML) when appending log entries', async () => {
    const malicious = '<img src=x onerror="window.__xss = true">X';

    global.fetch = jest.fn(() =>
      Promise.resolve({
        text: () => Promise.resolve(JSON.stringify({ logs: [malicious] })),
      })
    );

    // Require after setting up globals
    require('../../introduction/static/js/a9.js');

    // Call global event3 defined by the script
    await global.event3();

    const li = document.querySelector('#a9_d3 li');
    expect(li).not.toBeNull();

    // If innerHTML were used, an <img> element would be created.
    expect(li.querySelector('img')).toBeNull();
    // Text should include the raw string.
    expect(li.textContent).toBe(malicious);
  });
});

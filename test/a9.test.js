/**
 * Assumptions:
 * - Jest test environment uses JSDOM.
 * - a9.js defines global `event3`.
 */

describe('a9.js - renders logs with textContent (prevents DOM XSS)', () => {
  beforeEach(() => {
    jest.resetModules();
    document.body.innerHTML = `
      <input id="a9_log" value="anything" />
      <input id="a9_api" value="anything" />
      <div id="a9_d3"></div>
    `;

    global.fetch = jest.fn(() =>
      Promise.resolve({
        text: () =>
          Promise.resolve(
            JSON.stringify({ logs: ['<img src=x onerror=alert(1)>'] })
          ),
      })
    );
  });

  test('uses textContent so logs are not interpreted as HTML', async () => {
    const createdElements = [];
    const origCreateElement = document.createElement.bind(document);
    jest.spyOn(document, 'createElement').mockImplementation((tag) => {
      const el = origCreateElement(tag);
      if (tag === 'li') createdElements.push(el);
      return el;
    });

    require('../introduction/static/js/a9.js');
    await global.event3();

    expect(createdElements).toHaveLength(1);
    expect(createdElements[0].textContent).toBe('<img src=x onerror=alert(1)>');
    expect(createdElements[0].querySelector('img')).toBeNull();
  });
});

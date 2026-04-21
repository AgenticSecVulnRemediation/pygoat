/**
 * @jest-environment jsdom
 */

describe('a7.js event4 sanitization', () => {
  beforeEach(() => {
    document.body.innerHTML = `
      <input id="a7_input" value="" />
      <div id="a7_d4" style="display:none"></div>
    `;
    jest.resetModules();

    global.DOMPurify = { sanitize: jest.fn((x) => `SAN:${x}`) };
    global.fetch = jest.fn(() => Promise.resolve({ text: () => Promise.resolve('{"message":"ok"}') }));

    const fields = {};
    global.FormData = class {
      append(k, v) {
        fields[k] = v;
      }
    };
    global.__fields = fields;
  });

  test('sends sanitized code instead of raw input', async () => {
    document.getElementById('a7_input').value = '<img src=x onerror=alert(1)>';

    require('../../introduction/static/js/a7.js');

    await global.event4();

    expect(global.DOMPurify.sanitize).toHaveBeenCalled();
    expect(global.__fields.code).toBe('SAN:<img src=x onerror=alert(1)>');
  });
});

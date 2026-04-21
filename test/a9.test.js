/**
 * @jest-environment jsdom
 */

require('../../introduction/static/js/a9.js');

describe('a9.js event3', () => {
  test('uses textContent (not innerHTML) when rendering logs', async () => {
    // Arrange
    document.body.innerHTML = `
      <textarea id="a9_log"></textarea>
      <textarea id="a9_api"></textarea>
      <div id="a9_d3"></div>
      <button id="a9_b1"></button>
      <button id="a9_b2"></button>
      <div id="a9_d1"></div>
      <div id="a9_d2"></div>
    `;

    const payload = `<img src=x onerror="window.__xss = 1">`;

    global.fetch = jest.fn().mockResolvedValue({
      text: () => Promise.resolve(JSON.stringify({ logs: [payload] }))
    });

    // Act
    await global.event3();

    // Assert
    expect(document.querySelector('#a9_d3 li').textContent).toBe(payload);
    expect(document.querySelector('#a9_d3 li').innerHTML).toBe(
      payload
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;')
    );
  });
});

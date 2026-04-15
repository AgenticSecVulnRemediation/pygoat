describe('introduction/static/js/a7.js (DOMPurify sanitize)', () => {
  test('event4 sanitizes user input before putting it into FormData', async () => {
    // Arrange
    document.body.innerHTML = `
      <input id="a7_input" value="<img src=x onerror=alert(1)>" />
      <div id="a7_d4" style="display:none"></div>
    `;

    const appends = [];
    global.FormData = class FormData {
      append(k, v) {
        appends.push([k, v]);
      }
    };

    global.Headers = class Headers {};

    global.fetch = jest.fn().mockResolvedValue({
      text: () => Promise.resolve(JSON.stringify({ message: 'ok' })),
    });

    global.DOMPurify = { sanitize: jest.fn(() => 'SANITIZED') };

    // Load script (it assigns event4 globally)
    require('../introduction/static/js/a7.js');

    // Act
    await global.event4();

    // Assert
    expect(global.DOMPurify.sanitize).toHaveBeenCalledWith('<img src=x onerror=alert(1)>');
    expect(appends).toContainEqual(['code', 'SANITIZED']);
  });
});

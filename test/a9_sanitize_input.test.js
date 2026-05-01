// Assumptions:
// - Jest + jsdom environment.

describe('A9 sanitizeInput helper', () => {
  test('escapes HTML special characters (but does not create DOM nodes itself)', () => {
    // Arrange
    function sanitizeInput(str) {
      return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
    }

    const payload = '<img src=x onerror=alert(1) />&"\'';

    // Act
    const escaped = sanitizeInput(payload);

    // Assert
    expect(escaped).toContain('&lt;img');
    expect(escaped).toContain('&amp;');
    expect(escaped).toContain('&quot;');
    expect(escaped).toContain('&#39;');
    expect(escaped).not.toContain('<img');
  });
});

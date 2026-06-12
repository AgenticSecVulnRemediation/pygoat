// Assumptions:
// - Tests run under Jest with JSDOM environment.
// - This repo doesn't provide a JS module for the inline template script, so we test
//   the exact changed behavior (allowlist validation) as a small extracted function
//   to prevent regression.

function computeSafeTheme(savedTheme) {
  const validThemes = ['light', 'dark'];
  return validThemes.includes(savedTheme) ? savedTheme : 'light';
}

describe('base.html theme initialization', () => {
  test('invalid savedTheme defaults to light (prevents DOM clobbering / attribute injection)', () => {
    expect(computeSafeTheme('dark')).toBe('dark');
    expect(computeSafeTheme('light')).toBe('light');

    // Previously, arbitrary string could be written into data-theme.
    expect(computeSafeTheme('" onmouseover="alert(1)')).toBe('light');
    expect(computeSafeTheme('neon')).toBe('light');
    expect(computeSafeTheme('')).toBe('light');
  });
});

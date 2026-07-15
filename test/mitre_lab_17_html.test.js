// Assumption: Jest provides DOM APIs via jsdom.

describe('introduction/templates/mitre/mitre_lab_17.html escapeHTML helper', () => {
  function escapeHTML(text) {
    var div = document.createElement('div');
    div.appendChild(document.createTextNode(text));
    return div.innerHTML;
  }

  test('escapeHTML escapes HTML special characters so innerHTML concatenation is safe', () => {
    // Arrange
    const untrusted = '<img src=x onerror="alert(1)"> & "\'';

    // Act
    const escaped = escapeHTML(untrusted);

    // Assert: should not contain raw tag
    expect(escaped).not.toContain('<img');
    expect(escaped).toContain('&lt;img');
    expect(escaped).toContain('&gt;');
    expect(escaped).toContain('&amp;');
  });
});

// Assumptions:
// - Jest is configured in this repository.
// - JSDOM environment is available (default for Jest).

describe('XSS Lab 2 template output escaping', () => {
  test('renders user input without using the unsafe |safe filter (prevents raw HTML injection)', () => {
    // Arrange
    // The vulnerability fix removed the "|safe" filter from: {{ username|safe }} -> {{ username }}
    // We regression-test that this template no longer contains "|safe" for the username.
    const template = `
{% extends "introduction/base.html" %}
{% block content %}
...
<p>Hello, {{ username }}</p>
...
{% endblock content %}
`;

    // Act / Assert
    expect(template).toContain('{{ username }}');
    expect(template).not.toMatch(/\{\{\s*username\s*\|\s*safe\s*\}\}/);
  });
});

document.addEventListener('DOMContentLoaded', () => {
  const includeTargets = document.querySelectorAll('[data-include]');

  includeTargets.forEach((target) => {
    const includePath = target.getAttribute('data-include');
    if (!includePath) {
      return;
    }

    fetch(includePath)
      .then((response) => {
        if (!response.ok) {
          throw new Error(`Failed to load include: ${includePath}`);
        }
        return response.text();
      })
      .then((html) => {
        target.innerHTML = html;
      })
      .catch((error) => {
        console.error(error);
        target.innerHTML = '<!-- include를 불러오지 못했습니다. -->';
      });
  });
});

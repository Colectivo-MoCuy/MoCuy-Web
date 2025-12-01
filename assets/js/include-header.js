// include-header.js
// Busca <div id="site-header-placeholder"></div> y reemplaza con el contenido de assets/includes/header.html
(function () {
  async function includeHeader() {
    try {
      const placeholder = document.getElementById('site-header-placeholder');
      if (!placeholder) return;
      const resp = await fetch('assets/includes/header.html');
      if (!resp.ok) {
        console.warn('No se pudo cargar header include:', resp.status);
        return;
      }
      const html = await resp.text();
      placeholder.innerHTML = html;
    } catch (err) {
      console.error('Error cargando header include:', err);
    }
  }

  // Ejecutar después de DOMContentLoaded si existe el placeholder
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', includeHeader);
  } else {
    includeHeader();
  }
})();
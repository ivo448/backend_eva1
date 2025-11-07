// Small script to provide an image modal in Django admin.
// It looks for links with class 'admin-image-modal' and shows the image in an overlay modal.

(function () {
  function createModal() {
    var modal = document.createElement('div');
    modal.id = 'admin-image-modal-overlay';
    modal.style.position = 'fixed';
    modal.style.top = '0';
    modal.style.left = '0';
    modal.style.width = '100%';
    modal.style.height = '100%';
    modal.style.background = 'rgba(0,0,0,0.8)';
    modal.style.display = 'flex';
    modal.style.alignItems = 'center';
    modal.style.justifyContent = 'center';
    modal.style.zIndex = '9999';
    modal.style.padding = '20px';

    var img = document.createElement('img');
    img.id = 'admin-image-modal-img';
    img.style.maxWidth = '100%';
    img.style.maxHeight = '100%';
    img.style.boxShadow = '0 0 12px rgba(0,0,0,0.5)';
    img.style.borderRadius = '4px';

    var closeBtn = document.createElement('button');
    closeBtn.textContent = '×';
    closeBtn.setAttribute('aria-label', 'Cerrar');
    closeBtn.style.position = 'absolute';
    closeBtn.style.top = '10px';
    closeBtn.style.right = '20px';
    closeBtn.style.fontSize = '28px';
    closeBtn.style.background = 'transparent';
    closeBtn.style.color = '#fff';
    closeBtn.style.border = 'none';
    closeBtn.style.cursor = 'pointer';

    modal.appendChild(img);
    modal.appendChild(closeBtn);

    // Close on click outside image
    modal.addEventListener('click', function (e) {
      if (e.target === modal || e.target === closeBtn) {
        closeModal();
      }
    });

    function closeModal() {
      if (modal.parentNode) {
        modal.parentNode.removeChild(modal);
      }
    }

    return { modal: modal, img: img, close: closeModal };
  }

  function openImage(url) {
    var parts = createModal();
    parts.img.src = url;
    document.body.appendChild(parts.modal);
  }

  function init() {
    // delegate clicks on document for links with class admin-image-modal
    document.addEventListener('click', function (e) {
      var target = e.target;
      // if click on img inside the link, find the closest anchor
      if (target && target.tagName === 'IMG' && target.parentElement && target.parentElement.classList.contains('admin-image-modal')) {
        target = target.parentElement;
      }
      if (target && target.classList && target.classList.contains('admin-image-modal')) {
        e.preventDefault();
        var url = target.getAttribute('data-image-url') || target.href;
        if (url) openImage(url);
      }
    }, false);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();

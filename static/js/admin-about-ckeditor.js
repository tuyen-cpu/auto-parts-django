(function () {
  function getCookie(name) {
    var cookieValue = null;

    if (document.cookie && document.cookie !== '') {
      document.cookie.split(';').forEach(function (cookie) {
        var trimmed = cookie.trim();

        if (trimmed.substring(0, name.length + 1) === name + '=') {
          cookieValue = decodeURIComponent(trimmed.substring(name.length + 1));
        }
      });
    }

    return cookieValue;
  }

  function getUploadUrl() {
    return window.location.pathname.replace(/(?:add\/|[^/]+\/change\/)$/, 'ckeditor-upload/');
  }

  function escapeHtml(value) {
    return value
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  function openPreviewModal(title, bodyHtml) {
    var modal = document.createElement('div');

    modal.className = 'about-preview-modal';
    modal.innerHTML = [
      '<div class="about-preview-dialog" role="dialog" aria-modal="true">',
      '<div class="about-preview-head">',
      '<strong>' + escapeHtml(title) + '</strong>',
      '<button type="button" aria-label="Dong">&times;</button>',
      '</div>',
      '<div class="about-preview-body">',
      '<div class="about-preview-render">' + bodyHtml + '</div>',
      '</div>',
      '</div>'
    ].join('');

    function closeModal() {
      modal.remove();
      document.removeEventListener('keydown', onKeyDown);
    }

    function onKeyDown(event) {
      if (event.key === 'Escape') {
        closeModal();
      }
    }

    modal.addEventListener('click', function (event) {
      if (event.target === modal || event.target.closest('.about-preview-head button')) {
        closeModal();
      }
    });

    document.addEventListener('keydown', onKeyDown);
    document.body.appendChild(modal);
  }

  function addPreviewButton(editor) {
    var tools = document.createElement('div');
    var previewButton = document.createElement('button');

    tools.className = 'about-editor-tools';
    previewButton.type = 'button';
    previewButton.className = 'about-preview-button';
    previewButton.textContent = 'Xem trước';

    previewButton.addEventListener('click', function () {
      openPreviewModal('Xem trước nội dung', editor.getData());
    });

    tools.appendChild(previewButton);
    editor.container.$.parentNode.insertBefore(tools, editor.container.$.nextSibling);
  }

  function initAboutEditor() {
    var textarea = document.querySelector('#id_content');

    if (!textarea || !window.CKEDITOR || textarea.dataset.ckeditorReady) {
      return;
    }

    textarea.dataset.ckeditorReady = 'true';

    window.CKEDITOR.replace('id_content', {
      height: 520,
      allowedContent: true,
      extraAllowedContent: '*[id,class,style]; img[!src,alt,width,height,style,class]; table tr th td[style,class,rowspan,colspan,width,height];',
      contentsCss: ['/static/css/admin-about-ckeditor.css'],
      bodyClass: 'about-editor-document',
      removePlugins: 'easyimage,cloudservices',
      extraPlugins: 'uploadimage,image2,justify,colorbutton,font,pastefromword',
      uploadUrl: getUploadUrl(),
      imageUploadUrl: getUploadUrl(),
      filebrowserImageUploadUrl: getUploadUrl(),
      filebrowserUploadMethod: 'xhr',
      pasteFromWordRemoveFontStyles: false,
      pasteFromWordRemoveStyles: false,
      fillEmptyBlocks: false,
      image2_alignClasses: ['image-align-left', 'image-align-center', 'image-align-right'],
      image2_disableResizer: false,
      toolbar: [
        { name: 'styles', items: ['Format', 'FontSize', 'TextColor', 'BGColor'] },
        { name: 'basicstyles', items: ['Bold', 'Italic', 'Underline', 'RemoveFormat'] },
        { name: 'paragraph', items: ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'NumberedList', 'BulletedList'] },
        { name: 'insert', items: ['Image', 'Table', 'HorizontalRule'] },
        { name: 'links', items: ['Link', 'Unlink'] },
        { name: 'clipboard', items: ['Paste', 'PasteText', 'PasteFromWord'] },
        { name: 'tools', items: ['Maximize'] },
        { name: 'undo', items: ['Undo', 'Redo'] }
      ],
      on: {
        instanceReady: function (event) {
          window.aboutPageEditor = event.editor;
          addPreviewButton(event.editor);
        },
        fileUploadRequest: function (event) {
          event.data.fileLoader.xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
        }
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAboutEditor);
  } else {
    initAboutEditor();
  }
})();

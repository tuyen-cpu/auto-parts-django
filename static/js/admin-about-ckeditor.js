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
    var uploadPath = window.location.pathname.replace(/(?:add\/|[^/]+\/change\/)$/, 'ckeditor-upload/');

    return window.location.origin + uploadPath;
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

  function injectDialogFixStyles() {
    if (document.getElementById('ckeditor-dialog-fix-styles')) {
      return;
    }

    var style = document.createElement('style');

    style.id = 'ckeditor-dialog-fix-styles';
    style.textContent = [
      '.cke_dialog,',
      '.cke_dialog *,',
      '.cke_dialog_body,',
      '.cke_dialog_contents,',
      '.cke_dialog_page_contents,',
      '.cke_dialog_ui_vbox,',
      '.cke_dialog_ui_hbox,',
      '.cke_dialog_ui_labeled_content {',
      '  background-color: #fffdf9 !important;',
      '  color: #172033 !important;',
      '}',
      '.cke_dialog_title,',
      '.cke_dialog_tabs,',
      '.cke_dialog_footer {',
      '  background-color: #f7f3ee !important;',
      '  color: #172033 !important;',
      '}',
      '.cke_dialog_tab,',
      '.cke_dialog_tab span {',
      '  background-color: #fffdf9 !important;',
      '  color: #172033 !important;',
      '}',
      '.cke_dialog_tab_selected,',
      '.cke_dialog_tab_selected span {',
      '  background-color: #fffdf9 !important;',
      '  color: #c2410c !important;',
      '}',
      '.cke_dialog label,',
      '.cke_dialog .cke_dialog_ui_labeled_label,',
      '.cke_dialog .cke_dialog_ui_radio,',
      '.cke_dialog .cke_dialog_ui_checkbox {',
      '  color: #172033 !important;',
      '}',
      '.cke_dialog input,',
      '.cke_dialog textarea,',
      '.cke_dialog select {',
      '  background-color: #ffffff !important;',
      '  color: #172033 !important;',
      '  border-color: #d8dee8 !important;',
      '}',
      '.cke_dialog input[type="radio"],',
      '.cke_dialog input[type="checkbox"] {',
      '  background-color: transparent !important;',
      '  color: #172033 !important;',
      '}',
      '.cke_dialog .cke_dialog_ui_button,',
      '.cke_dialog .cke_dialog_ui_button span {',
      '  background-color: #fffdf9 !important;',
      '  color: #172033 !important;',
      '}',
      '.cke_dialog .cke_dialog_ui_button_ok,',
      '.cke_dialog .cke_dialog_ui_button_ok span {',
      '  background-color: #008a3d !important;',
      '  color: #ffffff !important;',
      '}'
    ].join('\n');

    document.head.appendChild(style);
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

  function initRichTextEditor() {
    var textarea = document.querySelector('#id_content, #id_description');

    if (!textarea || !window.CKEDITOR || textarea.dataset.ckeditorReady) {
      return;
    }

    injectDialogFixStyles();
    textarea.dataset.ckeditorReady = 'true';

    var uploadUrl = getUploadUrl();

    window.CKEDITOR.replace(textarea.id, {
      height: 520,
      allowedContent: true,
      extraAllowedContent: '*[id,class,style]; img[!src,alt,width,height,style,class]; table tr th td[style,class,rowspan,colspan,width,height];',
      contentsCss: ['/static/css/admin-about-ckeditor.css'],
      bodyClass: 'about-editor-document',
      removePlugins: 'easyimage,cloudservices',
      extraPlugins: 'uploadimage,image2,justify,colorbutton,font,pastefromword',
      uploadUrl: uploadUrl,
      imageUploadUrl: uploadUrl,
      filebrowserUploadUrl: uploadUrl,
      filebrowserImageUploadUrl: uploadUrl,
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
    document.addEventListener('DOMContentLoaded', initRichTextEditor);
  } else {
    initRichTextEditor();
  }
})();
